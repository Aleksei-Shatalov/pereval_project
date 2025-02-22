from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Database
from typing import Optional

app = FastAPI()

# Модель для данных перевала
class PerevalData(BaseModel):
    date_added: str
    raw_data: dict
    images: dict
    status: Optional[str] = 'new'

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