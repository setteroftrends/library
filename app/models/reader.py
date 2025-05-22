from sqlalchemy import Column, Integer, String
from ..core.base import Base


class Reader(Base):
    """
    id : int
        Primary key, auto-incremented.
    name : str
        Reader’s full name. Indexed for search.
    email : str
        Reader’s email address. Must be unique.
    """

    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    def model_dump(self):
        """
        Return dictionary representation of the reader instance.

        Returns:
            dict: Dictionary with keys 'id', 'name', 'email'.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
