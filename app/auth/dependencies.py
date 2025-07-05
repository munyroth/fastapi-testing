from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.utils import decode_token
from app.database import get_session
from app.models.user import User
from app.schemas.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    token_data = decode_token(token)
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return UserRead.model_validate(user, from_attributes=True)


async def get_current_active_user(
        current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    allowed_roles: list[str]

    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if not current_user.is_verified:
            raise HTTPException(
                status_code=403,
                detail="Account not verified. Please check your email for verification details."
            )
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action."
        )
