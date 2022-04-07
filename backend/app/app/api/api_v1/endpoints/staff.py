from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

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
def staff_list(*,
    db: Session = Depends(deps.get_db),
    _: models.Staff = Depends(deps.get_current_staff_user)
) -> Any:
    """
    Get all staff members
    """
    return crud.staff.get_multi(db)

@router.get("/students", response_model=List[schemas.Student])
def students(current_user: models.Staff = Depends(deps.get_current_staff_user)) -> Any:
    """
    Get all students for staff
    """
    return current_user.students


@router.put("/", response_model=schemas.Staff)
def update_staff(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Staff = Depends(deps.get_current_staff_user),
    staff_in: schemas.StaffUpdate,
) -> Any:
    """
    Update user object
    """

    staff = crud.staff.get(db, id=current_user.id)

    if staff_in.email is not None:
        staff.email = staff_in.email

    if staff_in.full_name is not None:
        staff.full_name = staff_in.full_name
    
    if staff_in.password is not None:
        staff.hashed_password = get_password_hash(staff_in.password)

    db.add(staff)
    db.commit()
    db.refresh(staff)
    
    return staff