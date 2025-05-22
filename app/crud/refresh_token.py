from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.refresh_token import RefreshToken


class RefreshTokenCRUD:
    """
    CRUD operations for the RefreshToken model.
    Handles creation, retrieval, and deletion of refresh tokens.
    """

    def __init__(self, db: Session):
        """
        Initialize the RefreshTokenCRUD with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.database: Session = db

    def create(self, refresh_token: Dict[str, Any]) -> Optional[RefreshToken]:
        """
        Create a new refresh token. If a token with the same value already exists, it will be replaced.

        Args:
            refresh_token (Dict[str, Any]): Dictionary with refresh token data.

        Returns:
            Optional[RefreshToken]: The newly created RefreshToken object.

        Raises:
            ValueError: If a token with the same value already exists.
            Exception: If another error occurs during the operation.
        """
        try:
            db_token = RefreshToken(**refresh_token)

            existing_token = self.get(refresh_token=refresh_token["token"])
            if existing_token:
                self.delete(existing_token.token)

            self.database.add(db_token)
            self.database.commit()
            self.database.refresh(db_token)
            return db_token

        except IntegrityError:
            self.database.rollback()
            raise ValueError("Refresh token already exists")

        except Exception as e:
            self.database.rollback()
            raise Exception(f"Failed to create refresh token: {str(e)}")

    def get(self, refresh_token: str = None, user_id: str = None) -> Optional[RefreshToken]:
        """
        Retrieve a refresh token by token value or user ID.

        Args:
            refresh_token (str, optional): The token string.
            user_id (str, optional): The user ID.

        Returns:
            Optional[RefreshToken]: The matched RefreshToken object, or None if not found.

        Raises:
            ValueError: If neither refresh_token nor user_id is provided.
        """
        if not (refresh_token or user_id):
            raise ValueError("Either refresh_token or user_id must be provided")

        if refresh_token:
            return self.database.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

        return self.database.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()

    def delete(self, refresh_token: str) -> bool:
        """
        Delete a refresh token by its token value.

        Args:
            refresh_token (str): The token string.

        Returns:
            bool: True if deletion was successful, False otherwise.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            result = self.database.query(RefreshToken).filter(RefreshToken.token == refresh_token).delete()
            self.database.commit()
            return result > 0

        except Exception as e:
            self.database.rollback()
            raise Exception(f"Failed to delete refresh token: {str(e)}")
