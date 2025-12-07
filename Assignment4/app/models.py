# Assignment4/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Хранение хешированного пароля
    hashed_password = Column(String, nullable=False)
    
    # Связь с историей входов
    history = relationship("LoginHistory", back_populates="user")

# Модель истории входов
class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Информация о браузере/ОС пользователя
    user_agent = Column(Text, nullable=True) 
    
    # Время входа (используем UTC)
    login_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Связь с пользователем
    user = relationship("User", back_populates="history")