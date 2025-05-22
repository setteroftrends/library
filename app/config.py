import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for application settings loaded from environment variables.

    Attributes:
        SECRET_KEY (str): Secret key used for cryptographic operations.
        SQLALCHEMY_DATABASE_URL (str): Database connection URL for SQLAlchemy.
        ALGORITHM (str): Algorithm used for token encoding (e.g., 'HS256').
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time for access tokens in minutes.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    class Config:
        """
        Inner Pydantic-style config for environment settings.
        """
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings:
    """
    Additional application settings.

    Attributes:
        REFRESH_TOKEN_EXPIRE_DAYS (int): Expiration time for refresh tokens in days.
    """
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
