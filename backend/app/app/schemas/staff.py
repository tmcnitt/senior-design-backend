from typing import Optional, List
from pydantic import BaseModel, EmailStr


# Shared properties
class StaffBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class StaffCreate(StaffBase):
    email: EmailStr
    full_name: str
    password: str


# Properties to receive via API on update
class StaffUpdate(StaffBase):
    password: Optional[str] = None


class StaffInDBBase(StaffBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Staff(StaffInDBBase):
    pass