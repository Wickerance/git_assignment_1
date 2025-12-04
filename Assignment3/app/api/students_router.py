# Assignment3/app/api/students_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import schemas
from ..services import student_service 

router = APIRouter()

# --- 1. Создать студента ---
@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Создать нового студента."""
    return student_service.create_student(db=db, student=student)

# --- 2. Получить список студентов ---
@router.get("/", response_model=List[schemas.Student])
def read_students_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех студентов."""
    students = student_service.get_students(db, skip=skip, limit=limit)
    return students

# --- 3. Получить информацию о студенте по его id ---
@router.get("/{student_id}", response_model=schemas.Student)
def read_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """Получить информацию о студенте по ID."""
    db_student = student_service.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

# --- 4. Удалить студента ---
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента по ID."""
    deleted_student = student_service.delete_student(db, student_id=student_id)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return

# --- 5. Добавить студента в группу ---
@router.put("/{student_id}/group/{group_id}", response_model=schemas.Student)
def add_student_to_group_endpoint(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """Добавить/перевести студента в указанную группу."""
    updated_student = student_service.add_student_to_group(db, student_id, group_id)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Студент или Группа не найдены")
    return updated_student

# --- 6. Удалить студента из группы ---
@router.delete("/{student_id}/group", response_model=schemas.Student)
def remove_student_from_group_endpoint(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента из его текущей группы."""
    updated_student = student_service.remove_student_from_group(db, student_id)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return updated_student

# --- 7. Перевести студента из группы A в группу B ---
# NOTE: Используем тот же эндпоинт, что и для добавления (PUT /{student_id}/group/{group_id})
# так как логика одна и та же: обновление group_id