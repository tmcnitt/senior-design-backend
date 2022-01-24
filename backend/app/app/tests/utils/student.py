import email
from typing import Dict, Tuple
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.tests.utils.utils import faker
from app.tests.utils.staff import staff_user

@pytest.fixture()
def student_user(db: Session, staff_user) -> Student:
    username = faker.email()
    password = faker.password()
    full_name = faker.name()


    user_in = StudentCreate(email=username, password=password, full_name=full_name)

    user = crud.student.create(db, obj_in=user_in, staff_id=staff_user.id)
    user.password = password
    
    yield user

    crud.student.remove(db=db, id=user.id)
