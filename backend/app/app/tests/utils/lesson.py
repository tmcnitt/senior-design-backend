import email
from typing import Dict, Tuple
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.lesson import Lesson
from app.crud.crud_lesson import LessonCreate

from app.tests.utils.utils import faker
from app.tests.utils.staff import staff_user

def make_single_lesson(db: Session, staff_id: int) -> Lesson:
    title = faker.company()
    content = faker.company()

    lesson_in = LessonCreate(title=title, staff_id=staff_id, content=content)

    user = crud.lesson.create(db, obj_in=lesson_in, staff_id=staff_id)

    return user


@pytest.fixture
def make_lesson(db: Session):
    def _make_lesson(staff_id: int):
        lesson = make_single_lesson(db, staff_id)
        return lesson
    
    yield _make_lesson


@pytest.fixture()
def lesson(db: Session, staff_user) -> Lesson:
    lesson = make_single_lesson(db, staff_user.id)
    
    yield lesson

    crud.lesson.remove(db=db, id=lesson.id)
