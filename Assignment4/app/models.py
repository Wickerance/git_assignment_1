from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# 用户模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # 存储哈希密码
    hashed_password = Column(String, nullable=False)
    
    # 定义与 LoginHistory 的关系
    history = relationship("LoginHistory", back_populates="user")

# 登录历史模型
class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 记录用户登录时使用的浏览器/操作系统信息
    user_agent = Column(Text, nullable=True) 
    
    # 记录登录时间
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 定义与 User 的关系
    user = relationship("User", back_populates="history")