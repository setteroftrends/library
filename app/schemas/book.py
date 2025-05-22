from pydantic import BaseModel

class BookCreate(BaseModel):
    """
    Schema for creating a new Book record.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        publication_year (int): The year the book was published.
        isbn (str): The unique ISBN identifier for the book.
        copies_available (int): Number of copies of the book available in the library.
    """

    title: str
    author: str
    publication_year: int
    isbn: str
    copies_available: int
