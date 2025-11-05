# Assignment3/app/main.py 

from fastapi import FastAPI
from db.database import init_db, engine
from db import models
from api import students_router, groups_router

# Создание всех таблиц в БД при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Студенческий API",
    description="API для управления студентами и группами (Задание 3)",
    version="1.0.0"
)

# Инициализация таблиц БД
@app.on_event("startup")
def on_startup():
    """Запускается при старте приложения"""
    init_db()
    print("База данных инициализирована.")

# Подключение роутеров
app.include_router(students_router.router, prefix="/students", tags=["Студенты"])
app.include_router(groups_router.router, prefix="/groups", tags=["Группы"])