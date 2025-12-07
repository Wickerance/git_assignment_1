# Assignment3/app/services/group_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db import models
from ..db import schemas

# --- Создать группу ---

def create_group(db: Session, group: schemas.GroupCreate) -> models.Group:
    """Создает новую группу в БД."""
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# --- Получить информацию о группе по id ---

def get_group(db: Session, group_id: int) -> Optional[models.Group]:
    """Получает информацию о группе по ее ID."""
    return db.query(models.Group).filter(models.Group.id == group_id).first()

# --- Получить список групп ---

def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[models.Group]:
    """Получает список всех групп."""
    return db.query(models.Group).offset(skip).limit(limit).all()

# --- Удалить группу ---

def delete_group(db: Session, group_id: int) -> Optional[models.Group]:
    """Удаляет группу и отменяет привязку всех студентов к этой группе."""
    db_group = get_group(db, group_id)
    if db_group:
        # Устанавливаем group_id в NULL для всех студентов этой группы
        db.query(models.Student).filter(models.Student.group_id == group_id).update({"group_id": None})
        
        db.delete(db_group)
        db.commit()
    return db_group

# --- Получить всех студентов в группе ---

def get_students_in_group(db: Session, group_id: int) -> List[models.Student]:
    """Получает всех студентов, принадлежащих указанной группе."""
    # Используем Eager Loading для загрузки информации о студентах
    return db.query(models.Student).filter(models.Student.group_id == group_id).all()