from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):

    def get_messages_to_student(self, db: Session, *, user_id: int) -> List[Message]:
        return db.query(Message).filter(Message.to_student_id == user_id).all()

    def get_messages_to_staff(self, db: Session, *, staff_id: int) -> List[Message]:
        return db.query(Message).filter(Message.to_staff_id == staff_id).all()

    def get_messages_from_student(self, db: Session, *, user_id: int) -> List[Message]:
        return db.query(Message).filter(Message.from_student_id == user_id).all()

    def get_messages_from_staff(self, db: Session, *, staff_id: int) -> List[Message]:
        return db.query(Message).filter(Message.from_staff_id == staff_id).all()

    def create(self, db: Session, *, obj_in: MessageCreate, user_type: str, user_id: int) -> Message:
        to_student_id = None
        to_staff_id = None
        if obj_in.to_user_type == "student":
            to_student_id = obj_in.to_user_id
        else:
            to_staff_id = obj_in.to_user_id

        from_student_id = None
        from_staff_id = None
        if user_type == "student":
            from_student_id = user_id
        else:
            from_staff_id = user_id
        
        db_obj = Message(
            message=obj_in.message,
            to_student_id=to_student_id,
            to_staff_id=to_staff_id,

            from_student_id=from_student_id,
            from_staff_id=from_staff_id,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self, 
    ):
       return



message = CRUDMessage(Message)
