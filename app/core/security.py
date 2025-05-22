from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from ..config import Config, Settings
from ..crud.refresh_token import RefreshTokenCRUD
from ..models.user import User
from ..schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/refresh")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain password matches the hashed password.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash the password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> Optional[User]:
    """
    Authenticate user by email and password.

    Args:
        email (str): User email.
        password (str): User password.
        db (Session): Database session.

    Returns:
        Optional[User]: User object if authentication succeeds, otherwise None.
    """
    from ..crud.user import UserCRUD

    user_crud = UserCRUD(db)
    return user_crud.authenticate_user(email, password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with expiration.

    Args:
        data (dict): Data to encode in the token (e.g., {'sub': email}).
        expires_delta (Optional[timedelta]): Token lifetime. Uses default if None.

    Returns:
        str: Encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)


def create_refresh_token(data: dict, db: Session) -> str:
    """
    Create a JWT refresh token, store it in the database, and delete any previous token for the user.

    Args:
        data (dict): Data to encode in the token (e.g., {'sub': email}).
        db (Session): Database session.

    Returns:
        str: Encoded JWT refresh token.
    """
    expire = datetime.now(tz=timezone.utc) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    refresh_token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    token_crud = RefreshTokenCRUD(db)
    last_token = token_crud.get(user_id=data["sub"])
    if last_token:
        token_crud.delete(last_token.token)

    token_crud.create({
        "token": refresh_token,
        "user_id": data["sub"],
        "expires_at": expire
    })

    return refresh_token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieve the current authenticated user based on the access token.

    Args:
        token (str): JWT access token extracted from the Authorization header.
        db (Session): Database session.

    Raises:
        HTTPException: If token is invalid or user not found.

    Returns:
        User: User object.
    """
    from ..crud.user import UserCRUD

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = UserCRUD(db).get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user


def refresh_tokens(refresh_token: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Refresh access and refresh tokens given a valid refresh token.

    Args:
        refresh_token (str): JWT refresh token.
        db (Session): Database session.

    Raises:
        HTTPException: If refresh token is invalid or expired.

    Returns:
        Dict[str, str]: Dictionary containing new access token, refresh token, and token type.
    """
    try:
        token_crud = RefreshTokenCRUD(db)

        if not token_crud.get(refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        payload = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        token_crud.delete(refresh_token)

        access_token = create_access_token(data={"sub": email})
        new_refresh_token = create_refresh_token(data={"sub": email}, db=db)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


def is_email(email: str) -> bool:
    """
    Validate whether a string is a properly formatted email address.

    Args:
        email (str): String to validate.

    Returns:
        bool: True if the string is a valid email, False otherwise.
    """
    import re
    pattern = r"^[-\w.]+@([-\w]+\.)+[-\w]{2,4}$"
    return re.match(pattern, email) is not None
