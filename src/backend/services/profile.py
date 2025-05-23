from datetime import timedelta
from fastapi.exceptions import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend import authentication
from backend.authentication import verify_password
from backend.config import settings
from backend.db.models import Profile
from backend.db.schemas.profile import ProfileRegister
from backend.redis.client import RedisClient
from .base import ServiceBase


class ProfileService(ServiceBase):
    async def get_by_phone(self, db: AsyncSession, phone: str) -> Profile:
        result = await db.scalars(
            select(self.model).where(Profile.phone == phone)
        )
        return result.first()

    async def get_by_email(self, db: AsyncSession, email: str) -> Profile:
        result = await db.scalars(
            select(self.model).where(Profile.email == email)
        )
        return result.first()

    async def check_existing_user(self, db: AsyncSession, phone: str):
        user = await self.get_by_phone(db, phone)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="These credentials are already occupied!",
            )

    async def register_user(
            self,
            db: AsyncSession,
            data: ProfileRegister,
    ) -> int:
        await self.check_existing_user(db, data.phone)
        if email := data.email:
            email_exists = await self.get_by_email(db, email)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already in use!",
                )

        data = data.model_dump(exclude_none=True)
        user = await self.create(db, obj_in=data)
        return user.id

    async def authenticate_user(
            self, db: AsyncSession, phone: str, password: str
    ) -> Profile | None:
        user = await self.get_by_phone(db, phone)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def update_refresh_token(
            redis: RedisClient,
            ttl: int,
            token_uuid: str,
            user
    ):
        redis.delete_refresh_token(str(user.id))
        redis.place_refresh_token(str(user.id), ttl, token_uuid)

    @staticmethod
    def current_refresh_token(user_id: int, redis: RedisClient):
        return redis.get_refresh_token(str(user_id))

    async def get_access_refresh_token(self, user: Profile, red: RedisClient):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token, _ = await authentication.generate_token(
            data={"sub": user.phone, "type": "access"},
            expires_delta=access_token_expires,
            type='access'
        )

        refresh_token_expires = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        refresh_token, code = await authentication.generate_token(
            data={"sub": user.phone, "type": "refresh"},
            expires_delta=refresh_token_expires,
            type='refresh',
        )
        self.update_refresh_token(
            red,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            code,
            user
        )
        return {"access": access_token, "refresh": refresh_token}


profile = ProfileService(Profile)
