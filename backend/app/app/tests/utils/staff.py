import email
from typing import Dict, Tuple
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from app.tests.utils.utils import faker





@pytest.fixture()
def staff_user(db: Session) -> Staff:
    username = faker.email()
    password = faker.password()
    full_name = faker.name()

    user_in = StaffCreate(email=username, password=password, full_name=full_name)
    user = crud.staff.create(db=db, obj_in=user_in)
    user.password = password
    
    yield user

    crud.staff.remove(db=db, id=user.id)

def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    return

    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
