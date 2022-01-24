from typing import Any, List

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
    user = crud.student.create(db, obj_in=student_in, staff=current_staff)

    if settings.EMAILS_ENABLED and student_in.email:
        send_new_account_email(
            email_to=student_in.email, username=student_in.email, password=student_in.password
        )
    
    return user

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.student.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/test-token", response_model=schemas.Student)
def test_token(current_user: models.Student = Depends(deps.get_current_student_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.get("/me", response_model=schemas.Student)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_student_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=schemas.Student)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    current_user: models.User = Depends(deps.get_current_student_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password

    user = crud.student.update(db, db_obj=current_user, obj_in=user_in)
    return user


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
    
    user_data = jsonable_encoder(user)
    user_data.staff_id = new_staff_id

    user = crud.student.update(db, db_obj=user, obj_in=user_data)
    return user
