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

@router.get("/", response_model=List[schemas.Staff])
def students(*,
    db: Session = Depends(deps.get_db),
    _: models.Staff = Depends(deps.get_current_staff_user)
) -> Any:
    return crud.staff.get_multi(db)

@router.get("/students", response_model=List[schemas.Student])
def students(current_user: models.Staff = Depends(deps.get_current_staff_user)) -> Any:
    return current_user.students