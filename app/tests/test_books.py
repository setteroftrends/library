import pytest
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
from app.schemas.borrowed_books import BorrowedBookCreate
from app.crud.book import BookCRUD


def test_borrow_fourth_book(client, test_books, test_reader, auth_headers, db_session):
    borrowing_data = {"book_id": test_books[3].id, "reader_id": test_reader.id}
    response = client.post("api/books/borrow/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() is True

    book = BookCRUD(db_session).get_by_id(test_books[3].id)
    assert book.copies_available == 2


def test_borrow_out_of_stock_book(client, test_books, test_reader, auth_headers):
    borrowing_data = {"book_id": test_books[2].id, "reader_id": test_reader.id}
    response = client.post("api/books/borrow/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "No available copies of the book"


def test_return_borrowed_book(client, test_books, test_reader, auth_headers, db_session):
    borrowing_data = {"book_id": test_books[3].id, "reader_id": test_reader.id}
    response = client.post("api/books/borrow/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 200

    response = client.post("api/books/return/", json=borrowing_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() is True

    book = BookCRUD(db_session).get_by_id(test_books[3].id)
<<<<<<< HEAD
    assert book.copies_available == 2
=======
from app.schemas.book import BookCreate
from app.crud.book import BookCRUD

@pytest.fixture
def new_book():
    return BookCreate(title="Test Book", author="Test Author", publication_year=2025, isbn="1234567890123", copies_available=5)

def test_create_book(client, new_book):
    response = client.post("/api/books/", json=new_book.model_dump())
    assert response.status_code == 201
    assert response.json()["title"] == new_book.title

def test_get_books(client):
    response = client.get("/api/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book(client):
    response = client.get("/api/books/1")
    assert response.status_code == 200
    assert "title" in response.json()

def test_delete_book(client):
    response = client.delete("/api/books/1")
    assert response.status_code == 204
>>>>>>> origin/master
=======
    assert book.copies_available == 2
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
