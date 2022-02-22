from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from datetime import timedelta
from app.core import security

router = APIRouter()

@router.get("/", response_model=List[schemas.Message])
def inbox(
    *,
    db: Session = Depends(deps.get_db),
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user),
) -> Any:
    """
    Get message sent to user 
    """

    if isinstance(current_user, models.Student):
       return crud.message.get_messages_to_student(db, user_id=current_user.id)
    else:
       return crud.message.get_messages_to_staff(db, staff_id=current_user.id)
   

@router.post("/", response_model=schemas.Message)
def send(*,  db: Session = Depends(deps.get_db), current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user), message_in: schemas.MessageCreate) -> Any:
    """
        Send a message. to_user_type should either be student or staff
    """
    
    user_type = "staff"
    if isinstance(current_user, models.Student):
        user_type = "student"
    
    return crud.message.create(db, obj_in=message_in, user_type=user_type, user_id=current_user.id)

@router.get("/sent", response_model=List[schemas.Message])
def sent(*,
    db: Session = Depends(deps.get_db),
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user),
) -> Any:
    if isinstance(current_user, models.Student):
       return crud.message.get_messages_from_student(db, user_id=current_user.id)
    else:
       return crud.message.get_messages_from_staff(db, staff_id=current_user.id)

