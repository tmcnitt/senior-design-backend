from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class LessonStudent(Base):
    student_id = Column(ForeignKey('student.id'), primary_key=True)
    lesson_id = Column(ForeignKey('lesson.id'), primary_key=True)

    is_unlocked = Column(Boolean)
    due_date = Column(DateTime)