from sqlalchemy import Column, Integer, String, DateTime
from ..core.base import Base


class RefreshToken(Base):
    """
    id : int
        Primary key, auto-incremented.
    user_id : int
        ID of the user the token belongs to.
    token : str
        Unique refresh token string.
    expires_at : datetime
        Expiration date and time of the token.
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String, unique=True)
    expires_at = Column(DateTime)
