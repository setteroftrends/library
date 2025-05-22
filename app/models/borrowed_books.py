from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from ..core.base import Base


class BorrowedBooks(Base):
    """
    id : int
        Primary key, auto-incremented.
    reader_id : int
        ID of the reader who borrowed the book.
    book_id : int
        ID of the borrowed book.
    date_borrowed : datetime
        Timestamp when the book was borrowed. Defaults to current time.
    date_returned : datetime or None
        Timestamp when the book was returned. Can be null if not returned yet.
    """

    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer)
    book_id = Column(Integer)
    date_borrowed = Column(DateTime, default=datetime.now)
    date_returned = Column(DateTime, nullable=True, default=None)
