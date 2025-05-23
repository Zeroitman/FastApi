from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from backend import services
from backend.db.database import get_db
from backend.db.schemas.profile import ProfileRegister
from backend.db.schemas.token import (
    Token, TokenData, OAuth2PasswordRequestData
)
from backend.authentication import hashed_password, check_refresh_token
from backend.redis.client import RedisClient, get_redis

auth_routes = APIRouter()


@auth_routes.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {"id": 3456}
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "This credentials are already occupied!"}
                }
            },
        }
    },
    response_description='register user by phone and password'
)
async def register(
        registration_data: ProfileRegister,
        db: Session = Depends(get_db),
):
    registration_data.password = hashed_password(registration_data.password)

    profile_id = await services.profile.register_user(
        db, registration_data,
    )

    return {"id": profile_id}


@auth_routes.post(
    "/token/",
    response_model=Token,
    response_description='returns pair of access and refresh token',
    responses={
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "You were not authorized!"}
                }
            },
        },
    }
)
async def access_token(
        auth_data: OAuth2PasswordRequestData = Depends(),
        db: Session = Depends(get_db),
        red: RedisClient = Depends(get_redis)
):
    user = await services.profile.authenticate_user(
        db, auth_data.phone, auth_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You were not authorized!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await services.profile.get_access_refresh_token(user, red)


@auth_routes.post(
    "/refresh/",
    response_model=Token,
    response_description='returns pair of access and refresh token'
)
async def refresh_token(
        auth_data: TokenData = Depends(),
        db: Session = Depends(get_db),
        red: RedisClient = Depends(get_redis)
):
    user = await check_refresh_token(auth_data.refresh, db, red)
    return await services.profile.get_access_refresh_token(user, red)
