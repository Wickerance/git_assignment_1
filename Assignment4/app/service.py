# Assignment4/app/service.py
from typing import Any 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models import User, LoginHistory
from app.schemas import UserAuth, Token, TokenRefresh
# Импортируем функции безопасности
from app.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    decode_token
)

# ===================================================
# Основная бизнес-логика: Регистрация
# ===================================================

async def register_new_user(user_data: UserAuth, db: AsyncSession) -> User:
    """Создает нового пользователя и сохраняет его в БД."""
    
    # 1. Проверка существования пользователя
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # 2. Хеширование пароля
    hashed_pass = hash_password(user_data.password)
    
    # 3. Создание объекта пользователя
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pass
    )
    
    # 4. Сохранение в БД
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

# ===================================================
# Основная бизнес-логика: Аутентификация
# ===================================================

async def authenticate_user(user_data: UserAuth, user_agent: str, db: AsyncSession) -> Token:
    """Проверяет учетные данные и генерирует JWT токены."""
    
    # 1. Поиск пользователя
    result = await db.execute(select(User).filter(User.email == user_data.email))
    user = result.scalars().first()
    
    # 2. Проверка пароля
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Запись истории входов
    history_entry = LoginHistory(
        user_id=user.id,
        user_agent=user_agent,
        login_time=datetime.now(timezone.utc)
    )
    db.add(history_entry)
    await db.commit()
    
    # 4. Генерация токенов
    # Access Token (короткий): type="access"
    access_token_data: dict[str, Any] = {"user_id": user.id, "type": "access"}
    access_token = create_access_token(access_token_data)
    
    # Refresh Token (длинный): type="refresh"
    refresh_token_data: dict[str, Any] = {"user_id": user.id, "type": "refresh"}
    refresh_token = create_refresh_token(refresh_token_data) 
    
    return Token(access_token=access_token, refresh_token=refresh_token)

# ===================================================
# Основная бизнес-логика: Обновление токенов
# ===================================================

async def refresh_tokens(token_data: TokenRefresh, db: AsyncSession) -> Token:
    """
    Принимает Refresh Token, проверяет его и выдает новую пару токенов.
    """
    # 1. Декодирование Refresh Token
    payload = decode_token(token_data.refresh_token)
    
    # 2. Проверка: валидность и тип 'refresh'
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_sub = payload.get("sub")
    
    try:
        user_id = int(user_id_sub) 
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token contains invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Поиск пользователя
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
        
    # 4. TODO: [Redis] Здесь можно добавить проверку черного списка токенов

    # 5. Генерация новых токенов
    new_access_token_data: dict[str, Any] = {"user_id": user.id, "type": "access"}
    new_access_token = create_access_token(new_access_token_data)
    
    new_refresh_token_data: dict[str, Any] = {"user_id": user.id, "type": "refresh"}
    new_refresh_token = create_refresh_token(new_refresh_token_data)
    
    return Token(access_token=new_access_token, refresh_token=new_refresh_token)