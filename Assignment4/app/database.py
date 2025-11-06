import os
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import OperationalError

# --- 1. 配置常量和连接字符串 ---
# 从环境变量获取数据库连接信息 (必须匹配 docker-compose.yml 中设置的变量名)
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.environ.get("POSTGRES_DB", "authdb")
DB_HOST = os.environ.get("DB_HOST", "assignment4-db") # 默认值应为 docker-compose 服务名
DB_PORT = os.environ.get("DB_PORT", "5432")

# 构建异步 PostgreSQL 连接字符串 (使用 asyncpg 驱动)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 2. 基础模型类 ---
class Base(DeclarativeBase):
    """所有 SQLAlchemy 模型的基类"""
    pass

# --- 3. 数据库引擎和会话设置 ---

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL, 
    echo=False # 生产环境中建议设为 False
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # 避免在提交后导致懒加载问题
)

# --- 4. FastAPI 依赖注入函数 ---

async def get_async_session() -> AsyncSession:
    """
    FastAPI 依赖项函数：提供一个异步数据库会话给路由处理程序。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # 异步关闭会话
            await session.close() 

# --- 5. 数据库初始化函数 (供 main.py 中的 lifespan 调用) ---

async def init_db():
    """
    尝试连接数据库并创建所有表，包含重试逻辑以应对 DB 启动延迟。
    """
    MAX_RETRIES = 10
    RETRY_DELAY = 3   # 秒
    
    # 引入重试逻辑
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Database initialization attempt {attempt + 1}/{MAX_RETRIES}...")
            
            async with engine.begin() as conn:
                # 1. 检查连接是否成功
                await conn.execute(text("SELECT 1"))
                
                # 2. 导入所有模型，确保 Base 知道所有表
                # 注意：如果您的 main.py 已经导入了 models，则无需在此处再次导入
                # 推荐在 main.py 或其他主入口点导入一次 models。
                
                # 3. 创建所有未存在的表
                await conn.run_sync(Base.metadata.create_all)
                
            print("Database initialization complete.")
            return # 成功，退出函数
        
        except OperationalError as e:
            # OperationalError 通常表示连接被拒绝或数据库不可用
            if attempt < MAX_RETRIES - 1:
                print(f"Database connection failed: {e}. Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Database initialization failed permanently.")
                raise # 达到最大重试次数，抛出异常
        
        except Exception as e:
            print(f"An unexpected error occurred during database initialization: {e}")
            raise # 处理其他类型的异常