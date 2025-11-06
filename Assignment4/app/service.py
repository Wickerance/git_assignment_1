from typing import Optional, Any 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, LoginHistory
from app.schemas import UserAuth, Token, TokenRefresh
# 确保导入了所有必需的安全函数，特别是 decode_token
from app.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from fastapi import HTTPException, status
from datetime import datetime

# ===================================================
# 核心业务逻辑（用户注册）
# ===================================================

async def register_new_user(user_data: UserAuth, db: AsyncSession) -> User:
    """创建新用户并将其保存到数据库"""
    
    # 1. 检查用户是否已存在
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # 2. 哈希密码
    hashed_pass = hash_password(user_data.password)
    
    # 3. 创建新用户对象
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pass
    )
    
    # 4. 添加并保存到数据库
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

# ===================================================
# 核心业务逻辑（用户登录）
# ===================================================

async def authenticate_user(user_data: UserAuth, user_agent: str, db: AsyncSession) -> Token:
    """验证用户凭证，并生成 JWT 令牌"""
    
    # 1. 查询用户
    result = await db.execute(select(User).filter(User.email == user_data.email))
    user = result.scalars().first()
    
    # 2. 检查用户是否存在或密码是否匹配
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. 记录登录历史
    history_entry = LoginHistory(
        user_id=user.id,
        user_agent=user_agent,
        login_time=datetime.utcnow()
    )
    db.add(history_entry)
    await db.commit()
    
    # -----------------------------------------------------
    # 🌟 关键修正：明确指定 Token 类型
    # -----------------------------------------------------
    # Access Token (短有效期): type="access"
    access_token_data: dict[str, Any] = {"user_id": user.id, "type": "access"}
    access_token = create_access_token(access_token_data)
    
    # Refresh Token (长有效期): type="refresh"
    refresh_token_data: dict[str, Any] = {"user_id": user.id, "type": "refresh"}
    refresh_token = create_refresh_token(refresh_token_data) 
    
    # Pydantic Model Token 默认包含 token_type="bearer"
    return Token(access_token=access_token, refresh_token=refresh_token)

# ===================================================
# 核心业务逻辑（令牌刷新）
# ===================================================

async def refresh_tokens(token_data: TokenRefresh, db: AsyncSession) -> Token:
    """
    接收 Refresh Token，验证后生成新的 Access Token 和 Refresh Token。
    """
    # 1. 解码 Refresh Token
    payload = decode_token(token_data.refresh_token)
    
    # 2. 验证：是否有效、是否为 Refresh 类型
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_sub = payload.get("sub")
    
    try:
        # Sub 字段存储的是 user_id
        user_id = int(user_id_sub) 
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing or contains invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 查找用户 (确保用户仍然存在)
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
        
    # 4. TODO: [Redis要求] 在这里集成 Redis 黑名单检查

    # 5. 生成新的 Token
    # -----------------------------------------------------
    # 🌟 关键修正：明确指定 Token 类型
    # -----------------------------------------------------
    new_access_token_data: dict[str, Any] = {"user_id": user.id, "type": "access"}
    new_access_token = create_access_token(new_access_token_data)
    
    new_refresh_token_data: dict[str, Any] = {"user_id": user.id, "type": "refresh"}
    new_refresh_token = create_refresh_token(new_refresh_token_data)
    
    return Token(access_token=new_access_token, refresh_token=new_refresh_token)