from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.database import get_session
from app.models.user import User
from app.schemas.schemas import CreateUser, BaseResponse, UserRead
from app.services.user import UserService

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_active_user)]


@cbv(router)
class UserRoutes:
    session: AsyncSession = Depends(get_session)

    @property
    def user_service(self):
        return UserService(self.session)

    @router.get("/info", response_model=BaseResponse[UserRead])
    async def read_user_info(self, current_user: UserDep):
        return BaseResponse(message="User info fetched successfully", data=current_user)

    @router.post("/", response_model=User)
    async def create_user(self, user: CreateUser):
        return await self.user_service.create(user)

    @router.get("/", response_model=list[User])
    async def read_users(self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
        return await self.user_service.get_all(offset, limit)

    @router.get("/{user_id}", response_model=User)
    async def read_user(self, user_id: str):
        return await self.user_service.get_by_id(user_id)

    @router.delete("/{user_id}")
    async def delete_user(self, user_id: int):
        return await self.user_service.delete(user_id)
