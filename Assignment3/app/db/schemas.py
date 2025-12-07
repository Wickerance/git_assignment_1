# Assignment3/app/db/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# --- Базовые модели (Base Models) ---

class GroupBase(BaseModel):
    """Базовая схема для группы"""
    name: str = Field(..., description="Название группы")

class StudentBase(BaseModel):
    """Базовая схема для студента"""
    fio: str = Field(..., description="Полное имя (ФИО)")
    age: int = Field(..., description="Возраст")
    # group_id здесь не обязателен при создании, так как студент может быть без группы
    group_id: Optional[int] = Field(None, description="ID группы, к которой принадлежит студент")

# --- Модели для создания/ввода (Input Models) ---

class GroupCreate(GroupBase):
    """Схема для создания новой группы (POST)"""
    pass

class StudentCreate(StudentBase):
    """Схема для создания нового студента (POST)"""
    pass

# --- Модели для вывода (Output Models) ---

class Group(GroupBase):
    """Схема для вывода информации о группе"""
    id: int
    
    class Config:
        # Разрешает чтение данных из ORM объектов (SQLAlchemy моделей)
        # Pydantic v2 update: orm_mode replaced by from_attributes
        from_attributes = True

class Student(StudentBase):
    """Схема для вывода информации о студенте"""
    id: int
    
    # Вложенная схема для отображения информации о группе
    group: Optional[Group] = None
    
    class Config:
        from_attributes = True

# --- Модель для операций с группами ---

class StudentGroupUpdate(BaseModel):
    """Схема для добавления/перевода студента в группу"""
    # Этот group_id будет использоваться в пути URL или теле запроса
    group_id: int = Field(..., description="Целевой ID группы")