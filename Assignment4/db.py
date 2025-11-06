import os

# 导入 SQLAlchemy 核心组件
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import text, Column, Integer, String

# --- 1. 配置常量和连接字符串 ---
# 从环境变量获取数据库连接信息
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.environ.get("POSTGRES_DB", "authdb")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")

# 构建异步 PostgreSQL 连接字符串 (使用 asyncpg 驱动)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 2. 数据库引擎和会话设置 ---
async_engine = create_async_engine(
    DATABASE_URL, 
    echo=False # 设为 True 可打印所有执行的 SQL 语句
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- 3. 基础模型类 ---
class Base(DeclarativeBase):
    """所有 SQLAlchemy 模型的基类"""
    pass

# --- 4. 示例模型 (用于初始化时创建表) ---

class User(Base):
    """数据库中的用户表模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# --- 5. 数据库初始化函数 (供 main.py 中的 lifespan 调用) ---

async def initialize_database():
    """
    连接到数据库并创建所有表（如果它们尚不存在）。
    """
    # 使用 async_engine.begin() 启动一个事务
    async with async_engine.begin() as conn:
        # 1. 检查连接是否成功
        await conn.execute(text("SELECT 1"))
        
        # 2. 创建所有未存在的表
        # conn.run_sync() 用于在异步代码中执行同步的 create_all 方法
        await conn.run_sync(Base.metadata.create_all)

# --- 6. FastAPI 依赖注入函数 ---

async def get_async_session():
    """
    FastAPI 依赖项函数：提供一个异步数据库会话给路由处理程序。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()