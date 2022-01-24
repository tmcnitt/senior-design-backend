from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.staff import staff_user
from app.tests.utils.student import make_student, student_user
from app.tests.utils.utils import faker
from app.tests.utils.utils import authentication_headers

def test_create_student(
    client: TestClient,db: Session, staff_user
) -> None:
    staff_headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    username = faker.email()
    password = faker.password()
    full_name = faker.name()

    data = {"email": username, "password": password, "full_name": full_name}

    r = client.post(
        f"{settings.API_V1_STR}/students/", json=data,headers=staff_headers
    )
    assert 200 <= r.status_code < 300

    created_user = r.json()
    user = crud.student.get_by_email(db, email=username)

    assert user
    assert user.email == created_user["email"]
    assert user.full_name == created_user["full_name"]
    assert user.staff_id == staff_user.id


def test_get_classmates(
    client: TestClient, db: Session, staff_user, make_student
) -> None:

    students = [make_student(staff_user.id) for _ in range(5)]
    student = students[-1]    

    headers = authentication_headers(client, student.email, student.password, "student")


    r = client.get(
        f"{settings.API_V1_STR}/students/", headers=headers
    )
    assert 200 <= r.status_code < 300

    result = r.json()
    assert len(result) == 5





