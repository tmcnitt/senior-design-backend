from optparse import Option
from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class StudentBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    staff_id: Optional[int] = None


# Properties to receive via API on creation
class StudentCreate(StudentBase):
    email: EmailStr
    password: str
    staff_id: int


# Properties to receive via API on update
class StudentUpdate(StudentBase):
    password: Optional[str] = None


class StudentInDBBase(StudentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Student(StudentInDBBase):
    pass
