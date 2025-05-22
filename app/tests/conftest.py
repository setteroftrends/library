import pytest
from fastapi.testclient import TestClient
from app.main import app
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
from app.core.database import get_db
from app.models.user import User
from app.models.book import Book
from app.models.reader import Reader
from sqlalchemy.orm import Session
import uuid

# login or refresh and put token here
temp_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmdAZ21haWwuY29tIiwiZXhwIjoxNzQ3ODI2MDEzfQ.vqacrc-iy8kTNCTOXYzfGvbAwpeqbvLJltz0scytqmE"
<<<<<<< HEAD
=======
>>>>>>> origin/master
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
        yield c

@pytest.fixture(scope="module")
def db_session():
    db = next(get_db())
    yield db
    db.close()


@pytest.fixture(scope="module")
def test_user(db_session: Session):
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password="$2b$12$EEAWBfi1sbIeg.ySKetiVuQOtL4Gobjclxd27sCT0NjQBbGqN1WYS")  # Mock hashed password
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="module")
def test_books(db_session: Session):
    books = [
        Book(title="Book 1", author="Author 1", publication_year=2020, isbn=f"1234567890{uuid.uuid4().hex[:3]}", copies_available=5),
        Book(title="Book 2", author="Author 2", publication_year=2021, isbn=f"1234567891{uuid.uuid4().hex[:3]}", copies_available=3),
        Book(title="Book 3", author="Author 3", publication_year=2022, isbn=f"1234567892{uuid.uuid4().hex[:3]}", copies_available=0),  # Out of stock
        Book(title="Book 4", author="Author 4", publication_year=2023, isbn=f"1234567893{uuid.uuid4().hex[:3]}", copies_available=2),
    ]
    db_session.add_all(books)
    db_session.commit()
    for book in books:
        db_session.refresh(book)
    return books

@pytest.fixture(scope="module")
def test_reader(db_session: Session):
    unique_email = f"reader_{uuid.uuid4()}@example.com"
    reader = Reader(name="Test Reader", email=unique_email)
    db_session.add(reader)
    db_session.commit()
    db_session.refresh(reader)
    return reader

@pytest.fixture(scope="module")
def auth_headers(client, test_user):
<<<<<<< HEAD
    return {"Authorization": f"Bearer {temp_access_token}"}
=======
        yield c
>>>>>>> origin/master
=======
    return {"Authorization": f"Bearer {temp_access_token}"}
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
