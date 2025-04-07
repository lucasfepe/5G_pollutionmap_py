import pytest
from app import app as fastapi_app


@pytest.fixture
def client():
    with fastapi_app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
