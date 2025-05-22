from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.token import TokenRefresh
from app.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    refresh_tokens,
    is_email
)
from app.core.database import get_db
from ..crud.user import UserCRUD
from ..schemas.user import UserCreate

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): User registration data containing email and password.
        db (Session): Database session dependency.

    Returns:
        User: Created user object.

    Raises:
        HTTPException 400: If email format is invalid or email already registered.
    """
    crud = UserCRUD(db)

    if not is_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(user=user)


@router.post("/login")
async def login(form_data: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate user and issue access and refresh tokens.

    Args:
        form_data (UserCreate): User login data (email and password).
        db (Session): Database session dependency.

    Returns:
        dict: Dictionary containing access_token, refresh_token, and token_type.

    Raises:
        HTTPException 401: If authentication fails due to incorrect email or password.
    """
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email}, db=db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(token: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh access and refresh tokens.

    Args:
        token (TokenRefresh): Refresh token schema with the current refresh token.
        db (Session): Database session dependency.

    Returns:
        dict: New access and refresh tokens.

    Raises:
        HTTPException: If token refresh fails (handled inside `refresh_tokens` function).
    """
    return refresh_tokens(token.refresh_token, db)
