from typing import Any, List, Union
from backend.app.app.models import staff

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

   
@router.post("/:id/lock/:studentid")
def lock(*,  
    db: Session = Depends(deps.get_db), 
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user), 
) -> Any:
    """
    Toggle lock for student id for lesson
    """
    pass

@router.post("/:id/due/:studentid")
def duedate(*,  
    db: Session = Depends(deps.get_db), 
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user), 
) -> Any:
    """
    Update due date for lesson for student
    """
    pass
