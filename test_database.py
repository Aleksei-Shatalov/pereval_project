import pytest
from database import Database, PerevalAdded

def test_add_pereval():
    db = Database()
    data = {
        "date_added": "2023-10-01T12:00:00",
        "raw_data": {"title": "Перевал Дятлова"},
        "images": {"image1": "base64_encoded_image_data"},
        "status": "new"
    }
    pereval_id = db.add_pereval(data)
    assert pereval_id is not None
    db.close()

def test_get_pereval_by_id():
    db = Database()
    pereval = db.get_pereval_by_id(1)
    assert pereval is not None
    assert pereval.raw_data["title"] == "Перевал Дятлова"
    db.close()

def test_update_pereval():
    db = Database()
    update_data = {"raw_data": {"title": "Обновлённый перевал"}}
    updated_pereval = db.update_pereval(1, update_data)
    assert updated_pereval is not None
    assert updated_pereval.raw_data["title"] == "Обновлённый перевал"
    db.close()