import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_submit_data():
    response = client.post("/submitData", json={
        "date_added": "2023-10-01T12:00:00",
        "raw_data": {"title": "Перевал Дятлова"},
        "images": {"image1": "base64_encoded_image_data"},
        "status": "new"
    })
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_pereval():
    response = client.get("/submitData/1")
    assert response.status_code == 200
    assert response.json()["raw_data"]["title"] == "Перевал Дятлова"

def test_update_pereval():
    response = client.patch("/submitData/1", json={
        "raw_data": {"title": "Обновлённый перевал"}
    })
    assert response.status_code == 200
    assert response.json()["state"] == 1

def test_get_pereval_by_email():
    response = client.get("/submitData/?user__email=user@example.com")
    assert response.status_code == 200
    assert len(response.json()) > 0