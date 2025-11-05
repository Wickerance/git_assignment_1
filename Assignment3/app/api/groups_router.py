# Assignment3/app/api/groups_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db import schemas
from ..services import student_service 
from ..services import group_service

router = APIRouter()

# --- 1. Создать группу ---
@router.post("/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_group_endpoint(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Создать новую группу."""
    return group_service.create_group(db=db, group=group)

# --- 2. Получить список групп ---
@router.get("/", response_model=List[schemas.Group])
def read_groups_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех групп."""
    groups = group_service.get_groups(db, skip=skip, limit=limit)
    return groups

# --- 3. Получить информацию о группе по ее id ---
@router.get("/{group_id}", response_model=schemas.Group)
def read_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """Получить информацию о группе по ID."""
    db_group = group_service.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

# --- 4. Удалить группу ---
@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """Удалить группу по ID."""
    deleted_group = group_service.delete_group(db, group_id=group_id)
    if deleted_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return

# --- 5. Получить всех студентов в группе ---
@router.get("/{group_id}/students", response_model=List[schemas.Student])
def get_students_in_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """Получить список всех студентов, принадлежащих указанной группе."""
    students = group_service.get_students_in_group(db, group_id=group_id)
    if not group_service.get_group(db, group_id=group_id):
        # Если группа не найдена, выбросим 404
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return students