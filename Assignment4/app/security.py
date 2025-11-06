from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

# 导入 FastAPI 认证相关依赖
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

# 配置 OAuth2 方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 配置密码哈希上下文
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    deprecated="auto"
)

# --------------------------------------------------
# JWT 配置 (已更新)
# --------------------------------------------------
SECRET_KEY = "YOUR_SUPER_SECRET_KEY" 
ALGORITHM = "HS256"
# 短期 Access Token (30 分钟)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 长期 Refresh Token (7 天)
REFRESH_TOKEN_EXPIRE_DAYS = 7

# --------------------------------------------------
# 数据库/用户模拟函数 (将在后续步骤中替换为真实 DB 查询)
# --------------------------------------------------

async def get_user_by_id(user_id: int):
    """模拟根据 ID 查找用户"""
    # ⚠️ 在实际应用中，您将使用 AsyncSession 和 ORM 查询。
    if user_id == 1:
        # 假设 ID 为 1 的用户是我们在注册时创建的那个
        return {"id": 1, "email": "final_success_pbkdf2@example.com"} 
    return None

# --------------------------------------------------
# 密码处理
# --------------------------------------------------

def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

# --------------------------------------------------
# Token 生成
# --------------------------------------------------

def create_access_token(data: dict) -> str:
    """创建 JWT Access Token (短期)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 负载中包含过期时间、主题(user_id)和类型 'access'
    to_encode.update({"exp": expire, "sub": str(data["user_id"]), "type": "access"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """创建 JWT Refresh Token (长期)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 负载中包含过期时间、主题(user_id)和类型 'refresh'
    to_encode.update({"exp": expire, "sub": str(data["user_id"]), "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --------------------------------------------------
# Token 验证与解码
# --------------------------------------------------

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码 JWT Token 并验证其有效性（签名、过期时间）。
    如果成功则返回 payload，否则返回 None。
    """
    try:
        # 解码并验证签名、过期时间
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token 无效（如过期、签名不匹配）
        return None

# --------------------------------------------------
# 依赖注入函数
# --------------------------------------------------

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    依赖注入函数，用于验证 Access Token 并获取当前用户。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. 解码和验证令牌
    payload = decode_token(token)
    
    # 2. 检查载荷是否存在、包含 'sub' 字段 (用户 ID) 且类型为 'access'
    if payload is None or "sub" not in payload or payload.get("type") != "access":
        raise credentials_exception
        
    user_id = int(payload.get("sub"))
    
    # 3. 查找用户
    user = await get_user_by_id(user_id) 
    
    if user is None:
        raise credentials_exception
        
    return user