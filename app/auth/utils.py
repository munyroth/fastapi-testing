import uuid
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = TokenData(
        iss=settings.JWT_ISSUER,
        sub=user_data["user_id"],
        exp=int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()),
        iat=int(datetime.now(timezone.utc).timestamp()),
        jti=str(uuid.uuid4()),
        scope=["refresh"] if refresh else ["access"],
    ).model_dump()

    token = jwt.encode(
        payload=payload, key=settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=settings.JWT_PUBLIC_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER,
        options={"require": ["exp", "iss", "sub"]}
    )
    return TokenData(**payload)
