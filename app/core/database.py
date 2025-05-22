from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.user import *
from app.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False  # Prevents objects from expiring after commit, useful in web apps
)


def get_db() -> Session:
    """
    Create and yield a new database session for a request, ensuring proper cleanup.

    This function provides a SQLAlchemy Session object that can be used
    to interact with the database within a request context.

    Yields:
        Session: A new SQLAlchemy Session object.

    The session is closed automatically when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Create all tables in the database using the metadata from SQLAlchemy models.

    This function will create tables that do not yet exist in the database
    according to the schema defined by SQLAlchemy models' Base metadata.

    It uses the engine bound to your database URL.
    """
    Base.metadata.create_all(bind=engine)


# Initialize tables on application startup
create_tables()
