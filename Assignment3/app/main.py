# Assignment3/app/main.py 

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.database import init_db, engine
from .db import models
from .api import students_router, groups_router

# Создание всех таблиц в БД при запуске (синхронно, если не используется миграция)
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения (замена @app.on_event).
    Запускается при старте, завершается при остановке.
    """
    # Действия при старте
    init_db()
    print("База данных инициализирована.")
    
    yield
    
    # Действия при остановке (если нужно)
    # print("Приложение останавливается...")

app = FastAPI(
    title="Студенческий API",
    description="API для управления студентами и группами (Задание 3)",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(students_router.router, prefix="/students", tags=["Студенты"])
app.include_router(groups_router.router, prefix="/groups", tags=["Группы"])