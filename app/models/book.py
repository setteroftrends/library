from sqlalchemy import Column, Integer, String
from ..core.base import Base


class Book(Base):
    """
    id : int
        Primary key, auto-incremented.
    title : str
        Book title; indexed to speed up search.
    author : str
        Author’s full name; indexed.
    publication_year : int
        Year the book was published; indexed for range queries.
    isbn : str
        International Standard Book Number; must be unique.
    copies_available : int
        Number of copies currently available for borrowing. Defaults to 1.
    description : str
        Free-text description or annotation of the book.
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer, index=True)
    isbn = Column(String, unique=True, index=True)
    copies_available = Column(Integer, index=True, default=1)
    description = Column(String)
