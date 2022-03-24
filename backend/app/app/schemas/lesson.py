from optparse import Option
from typing import Optional
from pydantic import BaseModel


class LessonBase(BaseModel):
    title: Optional[str]
    staff_id: Optional[int]
    content: Optional[str]


class LessonCreate(LessonBase):
    title: str
    content: str
    
class LessonUpdate(LessonBase):
    title: Optional[str] = None
    content: Optional[str] = None

class LessonInDBBase(LessonBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Lesson(LessonInDBBase):
    pass
