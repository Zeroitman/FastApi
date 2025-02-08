from enum import Enum
from typing import Optional
from fastapi import Body
from pydantic import BaseModel


class Token(BaseModel):
    access: Optional[str]
    refresh: Optional[str]


class OAuth2PasswordRequestData:
    def __init__(
        self,
        phone: str = Body(
            ...,
            media_type="application/json"
        ),
        password: str = Body(
            ...,
            media_type="application/json"
        ),
    ):
        self.phone = phone
        self.password = password


class TokenType(str, Enum):
    access = 'access'
    refresh = 'refresh'
