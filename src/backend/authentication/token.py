import uuid
from datetime import datetime, timedelta
from typing import Literal
import jwt
from backend.config import settings
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
