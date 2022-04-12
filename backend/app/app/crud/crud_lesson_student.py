from ast import Sub
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.lesson_student import LessonStudent
from app.schemas.lesson_student import LessonStudentCreate, LessonStudentUpdate, LessonStudentSummary
from app.models.student import Student
from app.models.submission import Submission

class CRUDLessonStudent(CRUDBase[LessonStudent, LessonStudentCreate, LessonStudentUpdate]):
    def delete_lesson(self, db:Session, *, lesson_id: int):
        db.query(LessonStudent).filter(LessonStudent.lesson_id == lesson_id).delete()
        db.commit()

    def delete_lesson_students(self, db:Session, *, lesson_id: int, student_id: int):
        db.query(LessonStudent).filter(and_(LessonStudent.lesson_id == lesson_id, LessonStudent.student_id == student_id)).delete()
        db.commit()

    def get_by_lesson_student(self, db:Session, *, lesson_id: int, student_id: int) -> LessonStudent:
        return db.query(LessonStudent).filter(and_(LessonStudent.lesson_id == lesson_id, LessonStudent.student_id == student_id)).first()
    
    def get_by_lesson_summary(self, db: Session, *, lesson_id: int):
        results = db.query(LessonStudent, Student.full_name, Submission).filter(Student.id == LessonStudent.student_id).filter(LessonStudent.lesson_id == lesson_id).outerjoin(Submission, and_(Submission.lesson_id == lesson_id, Submission.student_id == Student.id)).all()
        return results

    def get_by_lesson(self, db: Session, *, lesson_id: int) -> List[LessonStudent]:
        return db.query(LessonStudent).filter(LessonStudent.lesson_id == lesson_id).all()
    
    def create(self, db: Session, *, lesson_id: int, obj_in: LessonStudentCreate) -> LessonStudent:
        db_obj = LessonStudent(
            lesson_id=lesson_id,
            student_id=obj_in.student_id,
            due=obj_in.due,
            completed=obj_in.completed
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj



lesson_student = CRUDLessonStudent(LessonStudent)
