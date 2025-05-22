from pydantic import BaseModel

class ReaderCreate(BaseModel):
    """
    Schema for creating a new Reader.

    Attributes:
        name (str): Full name of the reader.
        email (str): Email address of the reader.
    """

    name: str
    email: str
