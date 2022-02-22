from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=False, nullable=False)

    to_student_id = Column(Integer, nullable=True)
    from_student_id = Column(Integer, nullable=True)

    to_staff_id = Column(Integer, nullable=True)
    from_staff_id = Column(Integer, nullable=True)