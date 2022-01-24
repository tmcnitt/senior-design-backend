from optparse import Option
from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class StudentBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class StudentCreate(StudentBase):
    email: EmailStr
    full_name: str
    password: str


# Properties to receive via API on update
class StudentUpdate(StudentBase):
    password: Optional[str] = None

class StudentStaffUpdate(StudentBase):
    staff_id: Optional[int] = None

class StudentInDBBase(StudentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class StudentInDB(StudentInDBBase):
    staff_id: Optional[int] = None

# Additional properties to return via API
class Student(StudentInDBBase):
    pass
