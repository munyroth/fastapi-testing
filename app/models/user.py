import uuid

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    password: str = Field(min_length=8)
    disabled: bool = False
    email: str | None = Field(index=True, unique=True, default=None, max_length=100)
    full_name: str | None = Field(default=None)
