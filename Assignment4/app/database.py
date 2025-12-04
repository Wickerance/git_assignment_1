# Assignment4/app/database.py
import os
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import OperationalError

# --- 1. Конфигурация и строка подключения ---
# Получение настроек БД из переменных окружения (должны совпадать с docker-compose.yml)
DB_USER = os.environ.get("POSTGRES_USER", "auth_user")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "auth_secure_pass")
DB_NAME = os.environ.get("POSTGRES_DB", "auth_service_db")
DB_HOST = os.environ.get("DB_HOST", "assignment4-db") # Имя сервиса в docker-compose
DB_PORT = os.environ.get("DB_PORT", "5432")

# Формирование URL подключения для драйвера asyncpg
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 2. Базовый класс моделей ---
class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass

# --- 3. Настройка движка и сессии ---

# Создание асинхронного движка
engine = create_async_engine(
    DATABASE_URL, 
    echo=False # В продакшене лучше ставить False
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # Избегаем проблем с lazy load после коммита
)

# --- 4. Зависимость FastAPI (Dependency) ---

async def get_async_session() -> AsyncSession:
    """
    Зависимость FastAPI: предоставляет асинхронную сессию БД для обработчиков роутов.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Асинхронное закрытие сессии
            await session.close() 

# --- 5. Инициализация БД (вызывается из lifespan в main.py) ---

async def init_db():
    """
    Попытка подключения к БД и создание таблиц.
    Включает логику повторных попыток (retry) для ожидания запуска БД.
    """
    MAX_RETRIES = 10
    RETRY_DELAY = 3   # секунды
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Попытка инициализации БД {attempt + 1}/{MAX_RETRIES}...")
            
            async with engine.begin() as conn:
                # 1. Проверка соединения
                await conn.execute(text("SELECT 1"))
                
                # 2. Создание всех таблиц, которые еще не существуют
                await conn.run_sync(Base.metadata.create_all)
                
            print("БД успешно инициализирована.")
            return # Успех, выход из функции
        
        except OperationalError as e:
            # OperationalError обычно означает, что БД еще не готова
            if attempt < MAX_RETRIES - 1:
                print(f"Ошибка подключения: {e}. Повтор через {RETRY_DELAY} сек...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                print("Превышено количество попыток. Не удалось инициализировать БД.")
                raise # Пробрасываем исключение после всех попыток
        
        except Exception as e:
            print(f"Неожиданная ошибка при инициализации БД: {e}")
            raise # Пробрасываем остальные ошибки