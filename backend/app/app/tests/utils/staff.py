import email
from typing import Dict, Tuple
from venv import create
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from app.tests.utils.utils import faker

def make_staff_user(db: Session) -> Staff:
    username = faker.email()
    password = faker.password()
    full_name = faker.name()

    user_in = StaffCreate(email=username, password=password, full_name=full_name)
    user = crud.staff.create(db=db, obj_in=user_in)
    user.password = password
    
    return user

@pytest.fixture
def make_staff(db: Session):
    created_staff = []

    def _make_staff():
        staff = make_staff_user(db)
        created_staff.append(staff)
        return staff
    
    yield _make_staff

    for staff in created_staff:
        crud.staff.remove(db=db, id=staff.id)

@pytest.fixture()
def staff_user(db: Session) -> Staff:
    user = make_staff_user(db)
    yield user
    crud.staff.remove(db=db, id=user.id)