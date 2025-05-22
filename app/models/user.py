from ..core.base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    """
    id : int
        Primary key, auto-incremented.
    email : str
        User's unique email address. Indexed for fast lookup.
    password : str
        Hashed password used for authentication.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
