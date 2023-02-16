from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base

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
