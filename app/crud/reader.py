from typing import Dict, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime, timezone
from ..schemas.reader import ReaderCreate
from ..models.reader import Reader
from ..models.borrowed_books import BorrowedBooks
from ..models.book import Book


class ReaderCRUD:
    """CRUD operations and business logic related to the Reader model."""

    def __init__(self, db: Session):
        """
        Initialize the CRUD class with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def create(self, reader: ReaderCreate) -> Reader:
        """
        Add a new reader to the database.

        Args:
            reader (ReaderCreate): Data for the new reader.

        Returns:
            Reader: The created Reader object.

        Raises:
            HTTPException: If a reader with the same email already exists
                           or if there is a database error.
        """
        try:
            db_reader = Reader(**reader.model_dump())
            self.db.add(db_reader)
            self.db.commit()
            self.db.refresh(db_reader)
            return db_reader
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Reader with this email already exists")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create reader: {str(e)}")

    def get_by_id(self, reader_id: int) -> Optional[Reader]:
        """
        Retrieve a reader by their ID.

        Args:
            reader_id (int): Reader's unique identifier.

        Returns:
            Optional[Reader]: Reader object if found, otherwise None.

        Raises:
            HTTPException: If the reader ID is invalid.
        """
        if not isinstance(reader_id, int) or reader_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid reader ID")

        return self.db.query(Reader).filter(Reader.id == reader_id).first()

    def get_by_email(self, email: str) -> Optional[Reader]:
        """
        Retrieve a reader by their email address.

        Args:
            email (str): Reader's email address.

        Returns:
            Optional[Reader]: Reader object if found, otherwise None.

        Raises:
            HTTPException: If the email is invalid.
        """
        if not email or not isinstance(email, str):
            raise HTTPException(status_code=400, detail="Invalid email")

        return self.db.query(Reader).filter(Reader.email == email).first()

    def get_by_username(self, username: str) -> Optional[Reader]:
        """
        Retrieve a reader by their username.

        Args:
            username (str): Reader's name.

        Returns:
            Optional[Reader]: Reader object if found, otherwise None.

        Raises:
            HTTPException: If the username is invalid.
        """
        if not username or not isinstance(username, str):
            raise HTTPException(status_code=400, detail="Invalid username")

        return self.db.query(Reader).filter(Reader.name == username).first()

    def get_all(self) -> Dict[int, Reader]:
        """
        Retrieve all readers from the database.

        Returns:
            Dict[int, Reader]: Dictionary mapping reader IDs to Reader objects.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            return {reader.id: reader for reader in self.db.query(Reader).all()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve readers: {str(e)}")

    def update(self, reader_id: int, reader_update: ReaderCreate) -> Optional[Reader]:
        """
        Update an existing reader's information.

        Args:
            reader_id (int): ID of the reader to update.
            reader_update (ReaderCreate): Updated reader data.

        Returns:
            Optional[Reader]: Updated Reader object if successful.

        Raises:
            HTTPException: If the reader does not exist, or if an update fails.
        """
        if not isinstance(reader_id, int) or reader_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid reader ID")

        try:
            db_reader = self.get_by_id(reader_id)
            if not db_reader:
                raise HTTPException(status_code=404, detail="Reader not found")

            update_data = reader_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_reader, key, value)

            self.db.commit()
            self.db.refresh(db_reader)
            return db_reader
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Email already in use")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update reader: {str(e)}")

    def delete(self, reader_id: int) -> bool:
        """
        Delete a reader by ID.

        Args:
            reader_id (int): Reader's ID.

        Returns:
            bool: True if deletion was successful, otherwise False.

        Raises:
            HTTPException: If the deletion fails or the ID is invalid.
        """
        if not isinstance(reader_id, int) or reader_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid reader ID")

        try:
            deleted = self.db.query(Reader).filter(Reader.id == reader_id).delete()
            self.db.commit()
            return bool(deleted)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete reader: {str(e)}")

    def have_borrowed_book(self, reader_id: int) -> bool:
        """
        Check whether the reader has borrowed any book.

        Args:
            reader_id (int): Reader's ID.

        Returns:
            bool: True if at least one book is borrowed, otherwise False.
        """
        return self.db.query(BorrowedBooks).filter(BorrowedBooks.reader_id == reader_id).first() is not None

    def borrow_book(self, reader_id: int, book_id: int) -> bool:
        """
        Register a book borrowing for the reader.

        Args:
            reader_id (int): Reader's ID.
            book_id (int): Book's ID.

        Returns:
            bool: True if borrowing succeeded.

        Raises:
            HTTPException: If reader or book not found, borrowing limit exceeded,
                           or the book is already borrowed.
        """
        try:
            reader = self.get_by_id(reader_id)
            if not reader:
                raise HTTPException(status_code=404, detail="Reader not found")

            book = self.db.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            if book.copies_available <= 0:
                raise HTTPException(status_code=400, detail="No available copies of the book")

            current_borrows = self.db.query(BorrowedBooks).filter(
                BorrowedBooks.reader_id == reader_id,
                BorrowedBooks.date_returned.is_(None)
            ).count()
            if current_borrows >= 3:
                raise HTTPException(status_code=400, detail="Reader has reached the borrowing limit of 3 books")

            borrow_record = BorrowedBooks(
                reader_id=reader_id,
                book_id=book_id,
                date_borrowed=datetime.now(tz=timezone.utc)
            )
            book.copies_available -= 1

            self.db.add(borrow_record)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Book is already borrowed by this reader")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to borrow book: {str(e)}")

    def return_borrowed_book(self, reader_id: int, book_id: int) -> bool:
        """
        Process the return of a previously borrowed book.

        Args:
            reader_id (int): Reader's ID.
            book_id (int): Book's ID.

        Returns:
            bool: True if the return was successful.

        Raises:
            HTTPException: If reader/book not found, or book was not borrowed.
        """
        try:
            reader = self.get_by_id(reader_id)
            if not reader:
                raise HTTPException(status_code=404, detail="Reader not found")

            book = self.db.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            borrow_record = self.db.query(BorrowedBooks).filter(
                BorrowedBooks.reader_id == reader_id,
                BorrowedBooks.book_id == book_id,
                BorrowedBooks.date_returned.is_(None)
            ).first()
            if not borrow_record:
                raise HTTPException(status_code=400, detail="Book was not borrowed by this reader or already returned")

            borrow_record.date_returned = datetime.now(tz=timezone.utc)
            book.copies_available += 1

            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to return book: {str(e)}")

    def get_borrowed_books(self, reader_id: int) -> List[Dict[str, Any]]:
        """
        Get a list of books borrowed by the reader.

        Args:
            reader_id (int): Reader's ID.

        Returns:
            List[Dict[str, Any]]: List of borrowed book records.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            return self.db.query(BorrowedBooks).filter(BorrowedBooks.reader_id == reader_id).all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve borrowed books: {str(e)}")
