# Assignment3/app/services/student_service.py
from sqlalchemy.orm import Session
from ..db import models
from ..db import schemas
from typing import List, Optional

# --- Создать студента ---

def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    """Создает нового студента в БД."""
    db_student = models.Student(fio=student.fio, age=student.age, group_id=student.group_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# --- Получить информацию о студенте по его id ---

def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    """Получает информацию о студенте по его ID."""
    # Используем .first() для получения одной записи
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# --- Получить список студентов ---

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    """Получает список всех студентов."""
    return db.query(models.Student).offset(skip).limit(limit).all()

# --- Удалить студента ---

def delete_student(db: Session, student_id: int) -> Optional[models.Student]:
    """Удаляет студента."""
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

# --- Добавить студента в группу ---

def add_student_to_group(db: Session, student_id: int, group_id: int) -> Optional[models.Student]:
    """Привязывает студента к указанной группе."""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.group_id = group_id
        db.commit()
        db.refresh(db_student)
    return db_student

# --- Удалить студента из группы ---

def remove_student_from_group(db: Session, student_id: int) -> Optional[models.Student]:
    """Удаляет студента из группы (устанавливает group_id в NULL)."""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.group_id = None
        db.commit()
        db.refresh(db_student)
    return db_student

# --- Перевести студента из группы A в группу B ---

def transfer_student(db: Session, student_id: int, new_group_id: int) -> Optional[models.Student]:
    """Переводит студента из текущей группы в новую."""
    # Это то же самое, что и добавление/обновление group_id
    return add_student_to_group(db, student_id, new_group_id)