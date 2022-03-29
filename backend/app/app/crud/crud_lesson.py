from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate
from app.models.lesson_student import LessonStudent


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):
    def get_by_student(self, db:Session, *, student_id: int) -> List[Lesson]:
        return db.query(Lesson).join(LessonStudent, LessonStudent.lesson_id == Lesson.id).filter(LessonStudent.student_id == student_id).all()

    def get_by_staff(self, db: Session, *, staff_id: int) -> List[Lesson]:
        return db.query(Lesson).filter(Lesson.staff_id == staff_id).all()

    def create(self, db: Session, *, obj_in: LessonCreate, staff_id: int) -> Lesson:
        db_obj = Lesson(
            title=obj_in.title,
            content=obj_in.content,
            staff_id=staff_id
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Lesson, obj_in: Union[LessonUpdate, Dict[str, Any]]
    ) -> Lesson:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


lesson = CRUDLesson(Lesson)
