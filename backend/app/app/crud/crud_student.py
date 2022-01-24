from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.student import Student
from app.models.staff import Staff
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Student]:
        return db.query(Student).filter(Student.email == email).first()

    def create(self, db: Session, *, obj_in: StudentCreate, staff: Staff) -> Student:
        db_obj = Student(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            staff_id=staff.id
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
        student = self.get_by_email(db, email=email)
        if not student:
            return None
        if not verify_password(password, student.hashed_password):
            return None
        return student



student = CRUDStudent(Student)
