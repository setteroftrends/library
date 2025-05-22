from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.database import get_db
from ..core.security import get_password_hash, verify_password


class UserCRUD:
    """
    CRUD operations for the User model.
    Handles user creation, retrieval, and authentication.
    """

    def __init__(self, db: Session = None):
        """
        Initialize the UserCRUD with a database session.

        Args:
            db (Session, optional): SQLAlchemy database session. If not provided, default session is used.
        """
        self.db: Session = db or get_db()

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            user (UserCreate): User data to be created.

        Returns:
            User: The newly created user instance.
        """
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email (str): User's email.

        Returns:
            Optional[User]: User instance if found, else None.
        """
        return self.db.query(User).filter(User.email == email).first()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by verifying email and password.

        Args:
            email (str): User's email address.
            password (str): Plain-text password to verify.

        Returns:
            Optional[User]: Authenticated user if credentials are valid, else None.
        """
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user
