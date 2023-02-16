from app import schemas
from tests.database import client, session
import pytest
from jose import jwt
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "abbas@gmail.com", "password": "1234"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "abbas@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    id = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/login", data={"username": "shahryar@gmail.com", "password": "Wrong password"})

    assert res.status_code == 403
    assert res.json().get('detail') == "invalid credentials"
