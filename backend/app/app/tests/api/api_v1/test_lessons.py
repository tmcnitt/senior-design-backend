from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.tests.utils.utils import faker
from app.tests.utils.staff import staff_user
from app.tests.utils.lesson import lesson, make_lesson

from app.tests.utils.utils import authentication_headers
from app.core.config import settings

def test_staff_create_lesson(
    staff_user,
    client: TestClient
) -> None:
    # Send the message 
    data = {
        "title": "Test Lesson", 
        "content": "This is a test lesson"
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/", json=data, headers=headers
    )

    assert 200 <= r.status_code < 300

    # Make sure it sent
    r = client.get(
        f"{settings.API_V1_STR}/lessons/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["title"] == "Test Lesson"
    assert result[0]["content"] == "This is a test lesson"

def test_staff_update_lesson(
    staff_user,
    lesson,
    client: TestClient
) -> None:
    # Send the message 
    update = {
        "title": "Test Lesson - Updated", 
        "content": "Test Content - Updated", 
    }

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.put(
        f"{settings.API_V1_STR}/lessons/{lesson.id}", json=update, headers=headers
    )

    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert result[1]["title"] == "Test Lesson - Updated"
    assert result[1]["content"] == "Test Content - Updated"



def test_staff_delete_lesson(
    db: Session,
    client: TestClient,
    make_lesson,
    staff_user
) -> None:

    lesson = make_lesson(staff_user.id)

    num_lessons = len(crud.lesson.get_by_staff(db, staff_id=staff_user.id))

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.delete(
        f"{settings.API_V1_STR}/lessons/{lesson.id}", headers=headers
    )

    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/", headers=headers
    )

    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == num_lessons-1
