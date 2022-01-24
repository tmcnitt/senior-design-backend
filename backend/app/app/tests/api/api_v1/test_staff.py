from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from faker import Faker


def test_create_staff(
    client: TestClient,db: Session, faker: Faker
) -> None:
    username = faker.email()
    password = faker.password()
    full_name = faker.name()

    data = {"email": username, "password": password, "full_name": full_name}

    r = client.post(
        f"{settings.API_V1_STR}/staff/", json=data,
    )
    assert 200 <= r.status_code < 300

    created_user = r.json()
    user = crud.staff.get_by_email(db, email=username)

    assert user
    assert user.email == created_user["email"]
    assert user.full_name == created_user["full_name"]



