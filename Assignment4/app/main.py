import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, APIRouter, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select # 这是一个未使用的导入，已移除

# ❗ 修正：将 .db 更改为 .database
# 并且导入新的初始化函数 init_db，并将其命名为 initialize_database
from .database import init_db as initialize_database, get_async_session 

# ❗ 修正：将 User 模型从 .models 中导入 (这是存放 ORM 模型的规范位置)
from .models import User 

# 导入其他应用模块
from .schemas import UserAuth, Token, TokenRefresh, UserBase
from .service import register_new_user, authenticate_user, refresh_tokens 
from .security import get_current_user

# ===================================================
# 数据库初始化生命周期函数 (现在只调用一次包含重试逻辑的函数)
# ===================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭事件的处理"""
    print("Waiting for PostgreSQL database to be ready and creating tables...")
    
    # 🌟 关键修正：直接调用 alias 后的 initialize_database 函数，
    # 该函数现在指向 database.py 中包含重试逻辑的 init_db()
    try:
        await initialize_database()
        print("Database initialization complete. Database tables created successfully!")
    except Exception as e:
        # 如果初始化失败，打印致命错误并允许应用崩溃 (Docker会处理重启)
        print(f"FATAL: Database initialization failed after all retries: {e}")
        raise e
        
    print("Starting Uvicorn...")
    yield
    print("Application shutting down...")
    
# ===================================================
# FastAPI 应用初始化
# ===================================================

# 传入 lifespan 函数
app = FastAPI(lifespan=lifespan, title="Auth Service")
router = APIRouter()

# ===================================================
# 核心认证端点 (路由保持不变)
# ===================================================

# 1. 注册用户
@router.post("/register")
async def register(
    user_data: UserAuth, 
    db: AsyncSession = Depends(get_async_session)
):
    """
    创建新用户并将其保存到数据库。
    """
    # 假设 register_new_user 位于 app/service.py
    await register_new_user(user_data, db)
    return {"message": "User registered successfully"}

# 2. 授权用户
@router.post("/login", response_model=Token)
async def login(
    user_data: UserAuth,
    user_agent: Annotated[str | None, Header()] = None, # 从请求头获取 User-Agent
    db: AsyncSession = Depends(get_async_session)
):
    """
    通过 email 和 password 登录，返回 access 和 refresh tokens。
    """
    if not user_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User-Agent header is required"
        )
        
    return await authenticate_user(user_data, user_agent, db)

# 3. 令牌更新 (新增)
@router.post("/refresh", response_model=Token)
async def refresh(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_async_session)
):
    """
    使用 Refresh Token 换取新的 Access Token 和 Refresh Token。
    """
    return await refresh_tokens(token_data, db)

# 4. 获取当前用户信息的受保护端点 (/me)
@router.get("/me", response_model=UserBase) # 假设返回 UserBase 模型
async def read_current_user(
    current_user: User = Depends(get_current_user) # get_current_user 返回 User ORM 对象
):
    """
    需要有效的 Access Token 才能访问，返回当前用户信息。
    """
    # 返回 UserBase 模型需要从 ORM 对象中提取数据
    return UserBase(email=current_user.email) 

# ===================================================
# 整合路由
# ===================================================
app.include_router(router)