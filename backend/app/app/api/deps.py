from typing import Generator, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> Union[models.Student, models.Staff]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = None
    if token_data.user_type == "student":
        user = crud.student.get(db, id=token_data.sub)
    elif token_data.user_type == "staff":
        user = crud.staff.get(db, id=token_data.sub)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate audience",
        )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_current_student_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Student:
    user = get_current_user(db, token)
    if isinstance(user, models.Student):
       return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is the wrong type",
        )

def get_current_staff_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Staff:
    user = get_current_user(db, token)
    if isinstance(user, models.Staff):
       return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is the wrong type",
        )

def get_selected_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),     
    current_staff: models.staff = Depends(get_current_staff_user), 
) -> models.Lesson:
    lesson = crud.lesson.get(db, id=lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson does not exist",
        )

    if lesson.staff_id != current_staff.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not your lesson;",
        )

    return lesson