# Assignment4/app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# ===================================================
# Схемы аутентификации (Authentication Schemas)
# ===================================================

class UserAuth(BaseModel):
    """Схема для регистрации и входа."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Схема для возврата токенов."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """Схема для обновления токена."""
    refresh_token: str

# ===================================================
# Схемы БД (Database Models)
# ===================================================

class UserBase(BaseModel):
    email: EmailStr

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

class LoginHistoryBase(BaseModel):
    user_id: int
    user_agent: str
    login_time: datetime

    class Config:
        from_attributes = True