from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
# Create database for test
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0014031681@localhost:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Testing
client = TestClient(app)


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)  # clear the tables
    # run our code before ew return our test
    Base.metadata.create_all(bind=engine)  # create the tables
    # run our code after test finishes
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "shahryar@gmail.com",
                 "password": "1234"}

    res = client.post("/users/", json=user_data)
    print("test")
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


# fixture for authorization
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_post(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']}]
    # }, {
    #     "title": "3rd title",
    #     "content": "3rd content",
    #     "owner_id": test_user2['id']
    # }]

    # map func
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
