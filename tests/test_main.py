#Testing is done through pytest. A simple 'pytest' command from the CLI starts all the tests.
import random
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database.base import Base, create_engine


#Test DB setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./tests/test_db.sqlite3"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

#Tests
def test_weather(test_db):
    response = client.get("/weather")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_data(test_db):
    response = client.get("/data", params={'n':random.randint(0, 100)})
    assert response.status_code == 200
    assert type(response.json()) == list