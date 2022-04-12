from optparse import Option
from typing import Optional, List, Tuple, Any
from pydantic import BaseModel
from datetime import datetime

from app.models.lesson_student import LessonStudent
from app.models.student import Student
from app.models.submission import Submission

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
    completed: Optional[bool] = False

    class Config:
        orm_mode = True


# Additional properties to return via API
class LessonStudent(LessonStudentInDBBase):
    pass

class LessonStudentSummary(LessonStudentInDBBase):
    results: List[Tuple[LessonStudent, str, Optional[str]]]

    class Config:
        orm_mode = True