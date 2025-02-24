from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from database import Database
from typing import Optional, List

app = FastAPI()

# Модель для данных перевала
class PerevalData(BaseModel):
    date_added: str
    raw_data: dict
    images: dict
    status: Optional[str] = 'new'

# Модель для обновления данных перевала
class PerevalUpdate(BaseModel):
    date_added: Optional[str]
    raw_data: Optional[dict]
    images: Optional[dict]
    status: Optional[str]

# Метод POST submitData
@app.post("/submitData")
async def submit_data(data: PerevalData):
    db = Database()
    try:
        pereval_id = db.add_pereval(data.dict())
        return {"status": 200, "message": "Данные успешно добавлены", "id": pereval_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# Метод GET /submitData/{id}
@app.get("/submitData/{id}")
async def get_pereval(id: int):
    db = Database()
    try:
        pereval = db.get_pereval_by_id(id)
        if not pereval:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        return {
            "id": pereval.id,
            "date_added": pereval.date_added,
            "raw_data": pereval.raw_data,
            "images": pereval.images,
            "status": pereval.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# Метод PATCH /submitData/{id}
@app.patch("/submitData/{id}")
async def update_pereval(id: int, data: PerevalUpdate):
    db = Database()
    try:
        pereval = db.get_pereval_by_id(id)
        if not pereval:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        # Проверяем, что запись в статусе "new"
        if pereval.status != "new":
            return {
                "state": 0,
                "message": "Запись нельзя редактировать, так как она не в статусе 'new'"
            }

        # Обновляем поля
        update_data = data.dict(exclude_unset=True)  # Исключаем поля, которые не были переданы
        db.update_pereval(id, update_data)

        return {
            "state": 1,
            "message": "Запись успешно обновлена"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# Метод GET /submitData/?user__email={email}
@app.get("/submitData/")
async def get_pereval_by_email(user__email: str = Query(..., description="Почта пользователя")):
    db = Database()
    try:
        perevals = db.get_pereval_by_email(user__email)
        if not perevals:
            raise HTTPException(status_code=404, detail="Записи не найдены")

        result = []
        for pereval in perevals:
            result.append({
                "id": pereval.id,
                "date_added": pereval.date_added,
                "raw_data": pereval.raw_data,
                "images": pereval.images,
                "status": pereval.status
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()