from typing import Dict, Generator

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sqlalchemy as sa

from app.core.config import settings
from app.db.testing import TestingSessionLocal, engine
from app.main import app
from app.api.deps import get_db

#from app.tests.utils.user import authentication_token_from_email
#from app.tests.utils.utils import get_superuser_token_headers
from app.db.base import Base


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c