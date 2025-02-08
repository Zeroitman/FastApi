import uuid
from datetime import datetime, timedelta
from typing import Literal
import jwt
from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend import services
from backend.config import settings
from backend.db.database import get_db
from backend.db.schemas.token import TokenType



async def generate_token(
        data: dict,
        expires_delta: timedelta,
        type: Literal[TokenType.access, TokenType.refresh]
) -> (str, uuid.UUID):
    uuid_code = None
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire.timestamp()})

    if type == TokenType.refresh:
        uuid_code = str(uuid.uuid4())
        to_encode.update({"uuid": uuid_code})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt, uuid_code


async def check_access_token(
        token: str = Header(
            ...,
            alias='Authorization',
            description="header for providing access token "
                        "in the format 'bearer {token}'"
        ),
        db: AsyncSession = Depends(get_db)
):
    token = token.lstrip('bearer').strip()
    return await check_token('access', token, db)


async def check_token(
        token_type_required: Literal[TokenType.access, TokenType.refresh],
        token: str,
        db: AsyncSession
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    now = datetime.utcnow()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception

        received_type: str = payload.get("type")
        if received_type != token_type_required:
            raise credentials_exception

        expire: datetime = datetime.fromtimestamp(payload.get("exp"))
        if now > expire:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    user = await services.profile.get_by_phone(db, phone=phone)
    if user is None:
        raise credentials_exception

    return user