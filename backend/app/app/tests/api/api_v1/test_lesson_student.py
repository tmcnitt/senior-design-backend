from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.tests.utils.utils import faker
from app.tests.utils.staff import staff_user
from app.tests.utils.lesson import lesson, make_lesson
from app.tests.utils.student import student_user

from app.tests.utils.utils import authentication_headers
from app.core.config import settings

import datetime

def test_add_delete_student(
    staff_user,
    student_user,
    lesson,
    client: TestClient
) -> None:
    data = {
        "due": str(datetime.datetime.now()), 
        "student_id": student_user.id,
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", json=data, headers=headers
    )

    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1

    r = client.delete(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/{student_user.id}", headers=headers
    )
    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 0



def test_change_due_and_done(
    db: Session,
    client: TestClient,
    student_user,
    lesson,
    staff_user
) -> None:
    data = {
        "due": str(datetime.datetime.now()), 
        "student_id": student_user.id,
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", json=data, headers=headers
    )

    assert 200 <= r.status_code < 300

    new_data = {
        "due": "2022-03-30T15:15:31.747676", 
        "completed": True,
    }

    r = client.put(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/{student_user.id}", headers=headers, json=new_data
    )

    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["due"] == new_data["due"]
    assert result[0]["completed"] == True


    r = client.delete(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/{student_user.id}", headers=headers
    )

def test_change_done(
    db: Session,
    client: TestClient,
    student_user,
    lesson,
    staff_user
) -> None:
    data = {
        "due": str(datetime.datetime.now()), 
        "student_id": student_user.id,
        "completed": True,
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", json=data, headers=headers
    )

    assert 200 <= r.status_code < 300

    new_data = {
        "due": "2022-03-30T15:15:31.747676", 
    }

    r = client.put(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/{student_user.id}", headers=headers, json=new_data
    )

    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["due"] == new_data["due"]
    assert result[0]["completed"] == True

    _ = client.delete(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/{student_user.id}", headers=headers
    )

def test_get_lesson(
    db: Session,
    client: TestClient,
    student_user,
    lesson,
    staff_user
) -> None:
    data = {
        "due": "2022-03-30T15:15:31.747676", 
        "student_id": student_user.id,
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", json=data, headers=headers
    )

    assert 200 <= r.status_code < 300

    headers = authentication_headers(client, student_user.email, student_user.password, "student")

    r = client.get(
        f"{settings.API_V1_STR}/lessons/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/status", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert result['due'] == data['due']

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}", headers=headers
    )

    assert 200 <= r.status_code < 300
    assert r.json()["id"] == lesson.id