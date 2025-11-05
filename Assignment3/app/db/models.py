# Assignment3/app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Group(Base):
    """Модель группы студентов"""
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    # Отношение (связь) с таблицей Student
    students = relationship("Student", back_populates="group")

class Student(Base):
    """Модель информации о студенте"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True, nullable=False) # ФИО
    age = Column(Integer, nullable=False)
    
    # Внешний ключ, связывающий с группой (groups.id)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True) # nullable=True - студент может быть без группы
    
    # Отношение (связь) с таблицей Group
    group = relationship("Group", back_populates="students")