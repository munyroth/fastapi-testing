from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr
from uuid import UUID

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    message: str
    data: T | None = None


class Register(BaseModel):
    username: str
    password: str
    full_name: str | None = None
    email: EmailStr | None = None


class Token(BaseModel):
    token_type: str = "Bearer"
    expires_in: int
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    iss: str
    sub: str
    exp: int
    iat: int
    jti: str
    scope: list[str]


class CreateUser(Register):
    disabled: bool | None = None


class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool
