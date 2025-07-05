from typing import Any, Coroutine

from fastapi import HTTPException
from sqlalchemy import Sequence
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.utils import generate_passwd_hash
from app.models.user import User
from app.schemas.schemas import CreateUser


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: CreateUser) -> User:
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password = generate_passwd_hash(user_data_dict["password"])

        self.session.add(new_user)

        await self.session.commit()

        return new_user

    async def get_all(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        result = await self.session.exec(select(User).offset(offset).limit(limit))
        return result.all()

    async def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        user = result.first()
        return user

    async def get_by_id(self, user_id: str) -> type[User]:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def delete(self, user_id: int) -> dict:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.session.delete(user)
        await self.session.commit()
        return {"ok": True}
