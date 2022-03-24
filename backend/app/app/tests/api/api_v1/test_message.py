from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import faker
from app.tests.utils.staff import make_staff_user, staff_user, make_staff
from app.tests.utils.student import student_user, make_student
from app.tests.utils.utils import authentication_headers

def test_staff_send_message(
    staff_user,
    student_user,
    client: TestClient,
    db: Session
) -> None:
    # Send the message 
    data = {"to_user_type": "student", "to_user_id": student_user.id, "message": "This is a test message"}

    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")

    r = client.post(
        f"{settings.API_V1_STR}/messages/", json=data, headers=headers
    )
    assert 200 <= r.status_code < 300

    # Make sure it sent
    r = client.get(
        f"{settings.API_V1_STR}/messages/sent", headers=headers
    )
    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["message"] == "This is a test message"

    # Make sure we got it
    headers = authentication_headers(client, student_user.email, student_user.password, "student")
    r = client.get(
        f"{settings.API_V1_STR}/messages/", headers=headers
    )
    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["message"] == "This is a test message"


def test_student_send_message(
    staff_user,
    student_user,
    client: TestClient,
    db: Session
) -> None:
    # Send the message 
    data = {"to_user_type": "staff", "to_user_id": staff_user.id, "message": "This is a test message.."}

    headers = authentication_headers(client, student_user.email, student_user.password, "student")

    r = client.post(
        f"{settings.API_V1_STR}/messages/", json=data, headers=headers
    )
    assert 200 <= r.status_code < 300

    # Make sure it sent
    r = client.get(
        f"{settings.API_V1_STR}/messages/sent", headers=headers
    )
    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["message"] == "This is a test message.."

    # Make sure we got it
    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")
    r = client.get(
        f"{settings.API_V1_STR}/messages/", headers=headers
    )
    assert 200 <= r.status_code < 300
    result = r.json()
    assert len(result) == 1
    assert result[0]["message"] == "This is a test message.."

