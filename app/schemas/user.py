from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (str): User's email address.
        password (str): User's password (plaintext before hashing).
    """
    email: str
    password: str
