import pytest
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
from app.core.security import create_access_token


def test_protected_endpoint_with_and_without_token(client, test_reader, auth_headers):
    response = client.get(f"api/reader/readers/{test_reader.id}", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    response = client.get(f"api/reader/readers/{test_reader.id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

<<<<<<< HEAD
=======
from fastapi import HTTPException
from app.schemas.user import UserCreate
from app.core.security import authenticate_user, create_access_token, create_refresh_token
from app.core.database import get_db

@pytest.mark.parametrize("email, password, expected_status", [
    ("testuser@example.com", "password123", 200),
    ("wronguser@example.com", "password123", 401),
])
def test_authenticate_user(client, email, password, expected_status):
    user_data = {"email": email, "password": password}
    response = client.post("/api/auth/login", json=user_data)
    assert response.status_code == expected_status
    if expected_status == 200:
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    else:
        assert response.json()["detail"] == "Incorrect email or password"
>>>>>>> origin/master
=======
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018

def test_create_access_token():
    data = {"sub": "testuser@example.com"}
    token = create_access_token(data)
<<<<<<< HEAD
<<<<<<< HEAD
    assert isinstance(token, str)
=======
    assert isinstance(token, str)

def test_create_refresh_token(db_session):
    data = {"sub": "testuser@example.com"}
    token = create_refresh_token(data, db_session)
    assert isinstance(token, str)
>>>>>>> origin/master
=======
    assert isinstance(token, str)
>>>>>>> 77d61d8118fb3c38e1b7d75a7661e84c72b51018
