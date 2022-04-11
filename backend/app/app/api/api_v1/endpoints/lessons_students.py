from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from datetime import timedelta
from app.core import security

router = APIRouter()

@router.get("/status", response_model=schemas.LessonStudent)
def student_status(*,  
    db: Session = Depends(deps.get_db), 
    lesson_id: int,
    current_user: models.Student = Depends(deps.get_current_student_user)
) -> Any:
    """
    Get the due date and completed status of a lesson for the logged in student
    """
    lesson = crud.lesson_student.get_by_lesson_student(db, lesson_id=lesson_id, student_id=current_user.id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not on lesson.",
        )
    
    return lesson

@router.get("/", response_model=List[schemas.LessonStudent])
def list(*,  
    db: Session = Depends(deps.get_db), 
    selected_lesson: models.Lesson = Depends(deps.get_selected_lesson)
) -> Any:
    """
    Get all students for this lesson
    """
    return crud.lesson_student.get_by_lesson(db, lesson_id=selected_lesson.id)

@router.post("/", response_model=schemas.LessonStudent)
def enable(*,  
    db: Session = Depends(deps.get_db), 
    lesson_student_in: schemas.LessonStudentCreate,
    selected_lesson: models.Lesson = Depends(deps.get_selected_lesson)
) -> Any:
    """
    Add a student to this lesson
    """
    return crud.lesson_student.create(db, lesson_id=selected_lesson.id, obj_in=lesson_student_in)


@router.put("/{student_id}", response_model=schemas.LessonStudent)
def change(*,  
    db: Session = Depends(deps.get_db), 
    lesson_student_in: schemas.LessonStudentUpdate,
    student_id: int,
    selected_lesson: models.Lesson = Depends(deps.get_selected_lesson)
) -> Any:
    """
    Modify the due date for this student
    """

    db_obj = crud.lesson_student.get_by_lesson_student(db, 
        lesson_id=selected_lesson.id, 
        student_id=student_id
    )

    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not on lesson.",
        )

    if lesson_student_in.due is not None:
        db_obj.due = lesson_student_in.due

    if lesson_student_in.completed is not None:
        db_obj.completed = lesson_student_in.completed

    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/{student_id}")
def delete(*,  
    student_id: int,
    db: Session = Depends(deps.get_db), 
    selected_lesson: models.Lesson = Depends(deps.get_selected_lesson),
) -> Any:
    """
    Remove a student from this lesson
    """
    crud.lesson_student.delete_lesson_students(db, 
        lesson_id=selected_lesson.id, 
        student_id=student_id
    )