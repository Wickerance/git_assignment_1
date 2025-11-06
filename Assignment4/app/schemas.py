from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ===================================================
# 认证模型 (Authentication Schemas)
# ===================================================

class UserAuth(BaseModel):
    """用于用户注册和登录的输入模型"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """登录成功后返回的 Access Token 和 Refresh Token 模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """用于 /refresh 端点接收 Refresh Token 的模型"""
    refresh_token: str

# ===================================================
# 用户和历史记录模型 (Database Models)
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