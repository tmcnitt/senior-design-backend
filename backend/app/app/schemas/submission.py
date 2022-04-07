from optparse import Option
from typing import Optional
from pydantic import BaseModel


class SubmissionBase(BaseModel):
    content: Optional[str]


class SubmissionCreate(SubmissionBase):
    content: str
    
class SubmissionInDBBase(SubmissionBase):
    id: int
    student_id: int
    content: str
    lesson_id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Submission(SubmissionInDBBase):
    pass
