from typing import Optional, Union

from pydantic import BaseModel
from .staff import Staff
from .student import Student


class TestTokenResponse(BaseModel):
    user_type: Optional[str] = None
    user: Optional[Union[Staff, Student]] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    user_type: Optional[str] = None

