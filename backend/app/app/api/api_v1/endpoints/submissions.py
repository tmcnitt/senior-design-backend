from datetime import timedelta
from sqlalchemy import and_
from typing import Any, Union, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()

@router.post("/", response_model=schemas.Submission)
def make_submission(
    *,
    db: Session = Depends(deps.get_db), 
    submission_in: schemas.SubmissionCreate,
    lesson_id: int,
    current_user: models.Student = Depends(deps.get_current_student_user), 
) -> Any:
    """
    Make new submission
    """
    lesson_student = crud.lesson_student.get_by_lesson_student(
        db, 
        lesson_id=lesson_id, 
        student_id=current_user.id
    )

    if lesson_student is None:
        raise HTTPException(
            status_code=401,
            detail="You do not have access to that lesson.",
        )

    db_obj = models.Submission (
        content = submission_in.content,
        lesson_id = lesson_id,
        student_id = current_user.id
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/submitted", response_model=Optional[schemas.Submission])
def list_submission(
    *,
    db: Session = Depends(deps.get_db), 
    lesson_id: int,
    current_user: models.Student = Depends(deps.get_current_student_user), 
) -> Any:
    """
    Get a submission for a student for a lesson if exists
    """
    submission = db.query(models.Submission).where(
        and_(models.Submission.lesson_id == lesson_id, models.Submission.student_id == current_user.id)
    ).first()

    return submission

@router.get("/", response_model=List[schemas.Submission])
def list_submissions(
    db: Session = Depends(deps.get_db), 
    selected_lesson: models.Lesson = Depends(deps.get_selected_lesson),
    current_user: models.Staff = Depends(deps.get_current_staff_user), 
) -> Any:
    """
    Get all submissions for a lesson
    """
    submissions = db.query(models.Submission).where(models.Submission.lesson_id == selected_lesson.id).all()
    return submissions
