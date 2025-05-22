from pydantic import BaseModel
from datetime import datetime


class BorrowedBookCreate(BaseModel):
    """
    Schema for creating a borrowed book record.

    Attributes:
        book_id (int): ID of the book being borrowed.
        reader_id (int): ID of the reader borrowing the book.
    """

    book_id: int
    reader_id: int
