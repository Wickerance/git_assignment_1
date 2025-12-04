# Assignment4/app/main.py
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, APIRouter, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Импорт локальных модулей
from .database import init_db as initialize_database, get_async_session 
from .models import User 
from .schemas import UserAuth, Token, TokenRefresh, UserBase
from .service import register_new_user, authenticate_user, refresh_tokens 
from .security import get_current_user

# ===================================================
# Управление жизненным циклом приложения (Lifespan)
# ===================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Действия при запуске и остановке приложения."""
    print("Ожидание готовности БД и создание таблиц...")
    
    try:
        await initialize_database()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось инициализировать БД: {e}")
        raise e
        
    print("Запуск сервера...")
    yield
    print("Остановка приложения...")
    
# ===================================================
# Инициализация FastAPI
# ===================================================

app = FastAPI(lifespan=lifespan, title="Auth Service")
router = APIRouter()

# ===================================================
# Эндпоинты (Endpoints)
# ===================================================

# 1. Регистрация
@router.post("/register")
async def register(
    user_data: UserAuth, 
    db: AsyncSession = Depends(get_async_session)
):
    """Регистрация нового пользователя."""
    await register_new_user(user_data, db)
    return {"message": "User registered successfully"}

# 2. Вход (Login)
@router.post("/login", response_model=Token)
async def login(
    user_data: UserAuth,
    user_agent: Annotated[str | None, Header()] = None, 
    db: AsyncSession = Depends(get_async_session)
):
    """Аутентификация пользователя и выдача токенов."""
    if not user_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User-Agent header is required"
        )
        
    return await authenticate_user(user_data, user_agent, db)

# 3. Обновление токена (Refresh)
@router.post("/refresh", response_model=Token)
async def refresh(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновление Access Token с помощью Refresh Token."""
    return await refresh_tokens(token_data, db)

# 4. Профиль пользователя (Protected)
@router.get("/me", response_model=UserBase)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Получение информации о текущем пользователе (требует авторизации)."""
    return UserBase(email=current_user.email) 

# Подключение роутера
app.include_router(router)