# Assignment3/app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings

# 1. Создание движка БД
engine = create_engine(settings.DATABASE_URL)

# 2. Создание фабрики локальных сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Базовый класс для объявления моделей ORM
Base = declarative_base()

# 4. Функция зависимости для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. Инициализация БД
def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)