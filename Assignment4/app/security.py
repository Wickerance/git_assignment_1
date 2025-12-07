# Assignment4/app/security.py
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

# Импорт зависимостей FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Импорт локальных модулей
from .database import get_async_session
from .models import User

# Настройка схемы OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Настройка контекста хеширования паролей
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    deprecated="auto"
)

# --------------------------------------------------
# Конфигурация JWT
# --------------------------------------------------
# ВАЖНО: Читаем секретный ключ из переменных окружения для безопасности
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_to_a_secure_key_in_production")
ALGORITHM = "HS256"

# Срок действия Access Token (30 минут)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Срок действия Refresh Token (7 дней)
REFRESH_TOKEN_EXPIRE_DAYS = 7

# --------------------------------------------------
# Работа с паролями
# --------------------------------------------------

def hash_password(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)

# --------------------------------------------------
# Генерация токенов
# --------------------------------------------------

def create_access_token(data: dict) -> str:
    """Создание JWT Access Token (короткоживущий)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # В payload добавляем срок действия, ID пользователя и тип 'access'
    to_encode.update({"exp": expire, "sub": str(data["user_id"]), "type": "access"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Создание JWT Refresh Token (долгоживущий)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # В payload добавляем срок действия, ID пользователя и тип 'refresh'
    to_encode.update({"exp": expire, "sub": str(data["user_id"]), "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --------------------------------------------------
# Валидация и декодирование токенов
# --------------------------------------------------

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Декодирует JWT токен и проверяет его валидность.
    Возвращает payload при успехе, иначе None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# --------------------------------------------------
# Зависимости (Dependencies)
# --------------------------------------------------

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Зависимость для проверки Access Token и получения текущего пользователя из БД.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Декодируем токен
    payload = decode_token(token)
    
    # 2. Проверяем наличие 'sub' (ID) и правильный тип токена ('access')
    if payload is None or "sub" not in payload or payload.get("type") != "access":
        raise credentials_exception
        
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise credentials_exception
    
    # 3. Ищем пользователя в базе данных
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user