from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.utils import verify_password, create_access_token
from app.database import get_session
from app.errors import InvalidCredentials
from app.schemas.schemas import Token
from app.services.user import UserService

router = APIRouter()

REFRESH_TOKEN_EXPIRY = 2


@cbv(router)
class AuthRoutes:
    session: AsyncSession = Depends(get_session)

    @property
    def user_service(self):
        return UserService(self.session)

    @router.post("/token", response_model=Token)
    async def login(
            self,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        user = await self.user_service.get_by_username(form_data.username)
        if not user:
            raise InvalidCredentials
        password_valid = verify_password(form_data.password, user.password)
        if not password_valid:
            raise InvalidCredentials

        access_token = create_access_token(
            user_data={
                "email": user.email,
                "user_id": str(user.id),
            }
        )

        refresh_token = create_access_token(
            user_data={"email": user.email, "user_id": str(user.id)},
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        )

        return Token(
            expires_in=REFRESH_TOKEN_EXPIRY * 24 * 60 * 60,
            access_token=access_token,
            refresh_token=refresh_token,
        )
