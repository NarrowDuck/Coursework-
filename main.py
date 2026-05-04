import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from dal.database import engine, Base
import dal.models  # <--- ЦЕЙ РЯДОК ОБОВ'ЯЗКОВИЙ! Без нього таблиці не створяться.

from ui.routes.auth_routes import router as auth_router
from ui.routes.queue_routes import router as queue_router

# Тепер база створить новий файл з усіма правильними таблицями
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Electronic Queue System")

app.mount("/static", StaticFiles(directory="ui/static"), name="static")

app.include_router(auth_router)
app.include_router(queue_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)