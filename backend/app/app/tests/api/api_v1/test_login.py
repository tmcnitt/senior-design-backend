from typing import Dict

from fastapi.testclient import TestClient

from app.tests.utils.staff import staff_user
from app.tests.utils.utils import authentication_headers
from sqlalchemy.orm import Session
from app.tests.utils.utils import faker

from app.core.config import settings


def test_get_access_token(client: TestClient, staff_user) -> None:
    login_data = {
        "username": staff_user.email,
        "password": staff_user.password,
        "scope": "staff"
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert tokens["user_type"] == "staff"

def test_cant_get_student_from_staff(client: TestClient, staff_user) -> None:
    login_data = {
        "username": staff_user.email,
        "password": staff_user.password,
        "scope": "student"
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


def test_use_access_token(
    client: TestClient, staff_user
) -> None:
    headers = authentication_headers(client, staff_user.email, staff_user.password, "staff")
    print(headers)
  
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token", headers=headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result['user_type'] == 'staff'
    assert result['user']
    assert result['user']['email'] == staff_user.email

