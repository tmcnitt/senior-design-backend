from optparse import Option
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LessonStudentBase(BaseModel):
    due: Optional[datetime] = None
    completed: Optional[bool] = None

class LessonStudentCreate(LessonStudentBase):
    student_id: int
    
class LessonStudentUpdate(LessonStudentBase):
    pass

class LessonStudentInDBBase(LessonStudentBase):
    lesson_id: str
    student_id: int
    due: datetime
    completed: bool

    class Config:
        orm_mode = True


# Additional properties to return via API
class LessonStudent(LessonStudentInDBBase):
    pass
