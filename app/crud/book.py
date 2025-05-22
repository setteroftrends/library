from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..schemas.book import BookCreate
from ..models.book import Book


class BookCRUD:
    def __init__(self, db: Session):
        """
        Initialize CRUD with a database session.

        Args:
            db (Session): SQLAlchemy session for DB operations.
        """
        self.db = db

    def create(self, book: BookCreate) -> Optional[Dict[str, Any]]:
        """
        Create a new book record in the database.

        Args:
            book (BookCreate): Data schema containing book details.

        Returns:
            Optional[Dict[str, Any]]: The created book object or None on failure.

        Raises:
            ValueError: If the book already exists.
            Exception: For other creation errors.
        """
        try:
            db_book = Book(
                title=book.title,
                author=book.author,
                publication_year=book.publication_year,
                isbn=book.isbn,
                copies_available=book.copies_available
            )
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)
            return db_book
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Book already exists")
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create book: {str(e)}")

    def get_all(self) -> Optional[List[Book]]:
        """
        Retrieve all book records from the database.

        Returns:
            Optional[Dict[str, Any]]: List of all book objects.
        """
        return self.db.query(Book).all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """
        Retrieve a single book by its ID.

        Args:
            book_id (int): Unique identifier of the book.

        Returns:
            Optional[Dict[str, Any]]: Book object if found, else None.
        """
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update(self, book_id: int, book: BookCreate) -> Optional[Dict[str, Any]]:
        """
        Update an existing book record by its ID.

        Args:
            book_id (int): Unique identifier of the book.
            book (BookCreate): Data schema containing updated book details.

        Returns:
            Optional[Dict[str, Any]]: Updated book object if successful.

        Raises:
            Exception: If update fails.
        """
        try:
            self.db.query(Book).filter(Book.id == book_id).update(book.model_dump())
            self.db.commit()
            return self.db.query(Book).filter(Book.id == book_id).first()
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update book: {str(e)}")

    def delete(self, book_id: int) -> None:
        """
        Delete a book record by its ID.

        Args:
            book_id (int): Unique identifier of the book to delete.

        Raises:
            Exception: If deletion fails.
        """
        try:
            self.db.query(Book).filter(Book.id == book_id).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete book: {str(e)}")
