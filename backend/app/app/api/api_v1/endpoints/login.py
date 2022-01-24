from datetime import timedelta
from typing import Any, Union

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


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests. Scope should either be student or staff
    """

    user = None
    scope = "student"

    if len(form_data.scopes) != 0:
        scope = form_data.scopes[0]
    
    if scope == "student":
        user = crud.student.authenticate(
            db, email=form_data.username, password=form_data.password
        )
    elif scope == "staff":
        user = crud.staff.authenticate(
            db, email=form_data.username, password=form_data.password
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid scope (either student or staff)")

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    #elif not crud.user.is_active(user):
    #    raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, scope, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "user_type": scope,
    }


@router.post("/login/test-token", response_model=schemas.TestTokenResponse)
def test_token(current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    scope = "student"
    if isinstance(current_user, models.Staff):
        scope = "staff"

    return schemas.TestTokenResponse(
       user_type=scope,
       user=current_user
    )


