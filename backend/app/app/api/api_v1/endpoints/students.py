from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core import security

router = APIRouter()


@router.post("/", response_model=schemas.Student)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    current_staff: models.Staff = Depends(deps.get_current_staff_user),
    student_in: schemas.StudentCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.student.get_by_email(db, email=student_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.student.create(db, obj_in=student_in, staff_id=current_staff.id)

    if settings.EMAILS_ENABLED and student_in.email:
        send_new_account_email(
            email_to=student_in.email, username=student_in.email, password=student_in.password
        )
    
    return user

@router.get("/", response_model=List[schemas.Student])
def classmates(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Student = Depends(deps.get_current_student_user),
) -> Any:
    """
    Get all classmates for a student
    """

    staff = current_user.staff
    return staff.students

@router.delete("/{user_id}")
def delete_student(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_staff: models.Staff = Depends(deps.get_current_staff_user),
) -> Any:
    """
    Delete a student
    """

    user = crud.student.get(db, id=user_id)

    if user is None:
        raise HTTPException(
            status_code=402,
            detail="That student does not exist.",
        )

    if user.staff_id != current_staff.id and not current_staff.is_admin:
        raise HTTPException(
            status_code=401,
            detail="You do not have permissions to update this student.",
        )

    crud.student.remove(db, id=user_id)

@router.put("/{user_id}/staff", response_model=schemas.Student)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    new_staff_id: int,
    current_staff: models.Staff = Depends(deps.get_current_staff_user),
) -> Any:
    """
    Update the staff member for a student
    """

    user = crud.student.get(db, id=user_id)

    if user.staff_id != current_staff.id and not current_staff.is_admin:
        raise HTTPException(
            status_code=401,
            detail="You do not have permissions to update this student.",
        )

    if crud.staff.get(db, new_staff_id) is None:
        raise HTTPException(
            status_code=400,
            detail="That staff member does not exist.",
        )
    
    user.staff_id = new_staff_id

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
