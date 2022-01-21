from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Student]:
        return db.query(Student).filter(Student.email == email).first()

    def create(self, db: Session, *, obj_in: StudentCreate) -> Student:
        db_obj = Student(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            staff_id=obj_in.staff_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Student, obj_in: Union[StudentUpdate, Dict[str, Any]]
    ) -> Student:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Student]:
        Student = self.get_by_email(db, email=email)
        if not Student:
            return None
        if not verify_password(password, Student.hashed_password):
            return None
        return Student

    def is_active(self, Student: Student) -> bool:
        return Student.is_active

    def is_superStudent(self, Student: Student) -> bool:
        return Student.is_superStudent


student = CRUDStudent(Student)
