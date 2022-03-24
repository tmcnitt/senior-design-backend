from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .staff import Staff  # noqa: F401
    from .lesson import Lesson  # noqa: F401
    from .lesson_student import LessonStudent  # noqa: F401

class Lesson(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False, nullable=False)
    content = Column(String, index=False, nullable=False)

    staff_id = Column(ForeignKey('staff.id'))