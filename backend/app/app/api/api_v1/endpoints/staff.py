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


@router.post("/", response_model=schemas.Staff)
def create_staff(
    *,
    db: Session = Depends(deps.get_db),
    staff_in: schemas.StaffCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.staff.get_by_email(db, email=staff_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.staff.create(db, obj_in=staff_in)
    if settings.EMAILS_ENABLED and staff_in.email:
        send_new_account_email(
            email_to=staff_in.email, username=staff_in.email, password=staff_in.password
        )
    
    return user

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.staff.authenticate(
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

@router.post("/login/test-token", response_model=schemas.Staff)
def test_token(current_user: models.Staff = Depends(deps.get_current_staff_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.get("/students", response_model=List[schemas.Student])
def students(current_user: models.Staff = Depends(deps.get_current_staff_user)) -> Any:
    return current_user.students