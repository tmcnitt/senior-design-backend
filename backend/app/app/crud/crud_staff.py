from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


class CRUDStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Staff]:
        return db.query(Staff).filter(Staff.email == email).first()

    def create(self, db: Session, *, obj_in: StaffCreate) -> Staff:
        db_obj = Staff(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_admin = False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Staff, obj_in: Union[StaffUpdate, Dict[str, Any]]
    ) -> Staff:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Staff]:
        staff = self.get_by_email(db, email=email)
        if not staff:
            return None

        if not verify_password(password, staff.hashed_password):
            return None

        return staff

    def is_admin(self, staff: Staff) -> bool:
        return staff.is_admin


staff = CRUDStaff(Staff)
