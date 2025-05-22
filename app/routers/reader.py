from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..core.database import get_db
from ..schemas.user import UserCreate
from ..schemas.reader import ReaderCreate
from ..crud.reader import ReaderCRUD

router = APIRouter()


@router.get("/readers/")
async def get_readers(db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Retrieve all readers from the database.

    Args:
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        List[Reader]: List of all reader records.
    """
    reader_crud = ReaderCRUD(db)
    return reader_crud.get_all()


@router.get("/readers/{reader_id}")
async def get_reader(reader_id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Retrieve a single reader by their ID.

    Args:
        reader_id (int): ID of the reader to retrieve.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Optional[Reader]: Reader object if found, else None.
    """
    reader_crud = ReaderCRUD(db)
    return reader_crud.get_by_id(reader_id)


@router.post("/readers/")
async def create_reader(reader: ReaderCreate, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Create a new reader entry.

    Args:
        reader (ReaderCreate): Reader data to create.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Reader: Created reader object.
    """
    reader_crud = ReaderCRUD(db)
    return reader_crud.create(reader)


@router.put("/readers/{reader_id}")
async def update_reader(reader_id: int, reader: ReaderCreate, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Update an existing reader's information.

    Args:
        reader_id (int): ID of the reader to update.
        reader (ReaderCreate): Updated reader data.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        Optional[Reader]: Updated reader object or None if not found.
    """
    reader_crud = ReaderCRUD(db)
    return reader_crud.update(reader_id, reader)


@router.delete("/readers/{reader_id}")
async def delete_reader(reader_id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    """
    Delete a reader by their ID.

    Args:
        reader_id (int): ID of the reader to delete.
        db (Session): Database session dependency.
        current_user (UserCreate): Currently authenticated user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    reader_crud = ReaderCRUD(db)
    return reader_crud.delete(reader_id)
