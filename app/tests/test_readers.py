import pytest
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
from app.schemas.borrowed_books import BorrowedBookCreate
from app.crud.reader import ReaderCRUD


def test_borrow_book_by_unregistered_reader(client, test_books, auth_headers):
    borrowing_data = {"book_id": test_books[0].id, "reader_id": 999}
    response = client.post("/borrow/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_borrowed_books(client, test_books, test_reader, auth_headers, db_session):
    borrowing_data = {"book_id": test_books[0].id, "reader_id": test_reader.id}
    response = client.post("api/books/borrow/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 200

    response = client.get(f"/api/books/readers/{test_reader.id}/borrowed/", headers=auth_headers)
    assert response.status_code == 200
    borrowed_books = response.json()
    assert len(borrowed_books) == 1
    assert borrowed_books[0]["book_id"] == test_books[0].id
    assert borrowed_books[0]["reader_id"] == test_reader.id
<<<<<<< HEAD
    assert borrowed_books[0]["date_returned"] is None
=======
from app.schemas.reader import ReaderCreate
from app.crud.reader import ReaderCRUD


@pytest.fixture
def new_reader():
    return ReaderCreate(name="Test Reader", email="reader@example.com")


def test_create_reader(client, new_reader):
    response = client.post("/api/reader/readers/", json=new_reader.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == new_reader.name


def test_get_readers(client):
    response = client.get("/api/reader/readers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_reader(client):
    response = client.get("/api/reader/readers/1")
    assert response.status_code == 200
    assert "name" in response.json()


def test_delete_reader(client):
    response = client.delete("/api/reader/readers/1")



>>>>>>> origin/master
=======
    assert borrowed_books[0]["date_returned"] is None
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
