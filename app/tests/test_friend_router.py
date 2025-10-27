from fastapi.testclient import TestClient
from io import BytesIO
import uuid
import pytest

from app.main import app  # твій FastAPI додаток

client = TestClient(app)

def test_create_friend():
    # Формуємо "файл" як BytesIO
    file_content = b"fake image content"
    file = BytesIO(file_content)
    file.name = "photo.jpg"  # обов'язково задаємо name

    response = client.post(
        "/friends/",  # твій роут
        data={
            "name": "John Doe",
            "profession": "Engineer",
            "profession_description": "Loves robots"
        },
        files={"photo": ("photo.jpg", file, "image/jpeg")}  # передаємо файл
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["profession"] == "Engineer"
    assert data["photo_url"]  # перевіряємо, що url повернувся


def test_fail_create_friend():
    response = client.post(
        "/friends/", data={}
    )

    assert response.status_code == 422

def test_get_friends():
    # Формуємо "файл" як BytesIO
    file_content = b"fake image content"
    file = BytesIO(file_content)
    file.name = "photo.jpg"  # обов'язково задаємо name

    response = client.post(
        "/friends/",  # твій роут
        data={
            "name": "John Doe",
            "profession": "Engineer",
            "profession_description": "Loves robots"
        },
        files={"photo": ("photo.jpg", file, "image/jpeg")}  # передаємо файл
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["profession"] == "Engineer"
    assert data["photo_url"]  # перевіряємо, що url повернувся

    _response = client.get(
        "/friends"
    )

    assert _response is not None
    data = _response.json()
    item = data["items"][0]
    assert item["name"] == "John Doe"