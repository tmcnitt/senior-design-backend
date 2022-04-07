from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db.base_class import Base

class Submission(Base):
    id = Column(Integer, primary_key=True, index=True)

    lesson_id = Column(ForeignKey('lesson.id'))
    student_id = Column(ForeignKey('student.id'))

    content = Column(String)