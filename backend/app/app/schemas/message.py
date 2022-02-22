from optparse import Option
from typing import Optional
from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str

# Properties to receive via API on creation
class MessageCreate(MessageBase):
    to_user_type: str
    to_user_id: int
    
class MessageUpdate(MessageBase):
    pass

class MessageInDBBase(MessageBase):
    id: int
    to_student_id: Optional[int]
    from_student_id: Optional[int]

    to_staff_id: Optional[int]
    from_staff_id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Message(MessageInDBBase):
    pass
