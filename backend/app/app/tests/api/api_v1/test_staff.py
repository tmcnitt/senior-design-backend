from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import faker
from app.tests.utils.staff import staff_user, make_staff
from app.tests.utils.student import student_user
from app.tests.utils.utils import authentication_headers

def test_create_staff(
    client: TestClient,db: Session
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



def test_get_students(
    client: TestClient, db: Session, student_user
):
    staff = student_user.staff
    headers = authentication_headers(client, staff.email, staff.password, "staff")

    r = client.get(
        f"{settings.API_V1_STR}/staff/students", headers=headers,
    )
    result = r.json()

    assert len(result) == 1
    assert result[0]['email'] == student_user.email
    assert result[0]['full_name'] == student_user.full_name
    assert result[0]['id'] == student_user.id


def test_move_student(
    client: TestClient, db: Session, student_user, make_staff
):
    new_staff = make_staff()
    old_staff = student_user.staff

    print("Old staff id: ", old_staff.id)
    print("New staff id: ", new_staff.id)

    assert old_staff.id != new_staff.id

    headers = authentication_headers(client, old_staff.email, old_staff.password, "staff")

    data = {"new_staff_id": new_staff.id}

    r = client.put(
        f"{settings.API_V1_STR}/students/{student_user.id}/staff", headers=headers,params=data
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_V1_STR}/staff/students", headers=headers,
    )
    result = r.json()
    assert len(result) == 0

    headers = authentication_headers(client, new_staff.email, new_staff.password, "staff")

    r = client.get(
        f"{settings.API_V1_STR}/staff/students", headers=headers,
    )
    result = r.json()

    assert len(result) == 1
    assert result[0]['email'] == student_user.email
    assert result[0]['full_name'] == student_user.full_name
    assert result[0]['id'] == student_user.id