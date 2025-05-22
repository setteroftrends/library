from fastapi import APIRouter, Depends
from ..core.database import get_db
from ..core.security import get_current_user

from ..models.book import Book
from ..schemas.book import BookCreate
from ..crud.book import BookCRUD

from ..schemas.borrowed_books import BorrowedBookCreate
from ..crud.reader import ReaderCRUD

from ..schemas.user import UserCreate

router = APIRouter()


@router.get("/")
def get_books(db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Retrieve all books from the database.

    Args:
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        List[Book]: List of all book records.
    """
    return BookCRUD(db).get_all()


@router.post("/")
def create_book(book: BookCreate, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Create a new book entry.

    Args:
        book (BookCreate): Book data to create.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Book: Created book object.
    """
    return BookCRUD(db).create(book)


@router.get("/{book_id}")
def get_book(book_id: int, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Retrieve a book by its ID.

    Args:
        book_id (int): ID of the book to retrieve.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Optional[Book]: Book object if found, else None.
    """
    return BookCRUD(db).get_by_id(book_id)


@router.delete("/{book_id}")
def delete_book(book_id: int, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Delete a book by its ID.

    Args:
        book_id (int): ID of the book to delete.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    return BookCRUD(db).delete(book_id)


@router.put("/{book_id}")
def update_book(book_id: int, book: BookCreate, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Update book information by ID.

    Args:
        book_id (int): ID of the book to update.
        book (BookCreate): New book data.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Optional[Book]: Updated book object or None if not found.
    """
    return BookCRUD(db).update(book_id, book)


@router.post("/borrow/")
def borrow_book(borrowed_book: BorrowedBookCreate, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Borrow a book for a reader.

    Args:
        borrowed_book (BorrowedBookCreate): Contains reader_id and book_id.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        bool: True if borrowing was successful.

    Raises:
        HTTPException: If borrowing fails due to validation or business logic.
    """
    return ReaderCRUD(db).borrow_book(borrowed_book.reader_id, borrowed_book.book_id)


@router.post("/return/")
def return_book(borrowed_book: BorrowedBookCreate, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Return a borrowed book for a reader.

    Args:
        borrowed_book (BorrowedBookCreate): Contains reader_id and book_id.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        bool: True if return was successful.

    Raises:
        HTTPException: If return fails due to validation or business logic.
    """
    return ReaderCRUD(db).return_borrowed_book(borrowed_book.reader_id, borrowed_book.book_id)


@router.get("/readers/{reader_id}/borrowed/")
def get_borrowed_books(reader_id: int, db=Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Get all books currently borrowed by a reader.

    Args:
        reader_id (int): ID of the reader.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        List[Dict]: List of borrowed book records for the reader.
    """
    return ReaderCRUD(db).get_borrowed_books(reader_id)
