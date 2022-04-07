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

def test_make_and_get_submission(
    staff_user,
    student_user,
    lesson,
    client: TestClient
) -> None:
    data = {
        "due": str(datetime.datetime.now()), 
        "student_id": student_user.id,
    }

    staff_headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")
    student_headers = authentication_headers(client, student_user.email, student_user.password, "student")

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/students/", json=data, headers=staff_headers
    )
    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/submissions/submitted", json=data, headers=student_headers
    )
    assert 200 <= r.status_code < 300
    assert r.json() == None

    data = {
        "content": "This is a test submission"
    }

    r = client.post(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/submissions/", json=data, headers=student_headers
    )
    assert 200 <= r.status_code < 300

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/submissions/", json=data, headers=staff_headers
    )
    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1

    r = client.get(
        f"{settings.API_V1_STR}/lessons/{lesson.id}/submissions/submitted", json=data, headers=student_headers
    )
    assert 200 <= r.status_code < 300
    assert r.json()['content'] == data['content']

   
