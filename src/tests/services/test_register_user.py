import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from tests.base import BaseTestCase
from tests.factories import ProfileFactory
from backend import services
from backend.db.schemas.profile import ProfileRegister
from backend.db.models import Profile, LocaleEnum


class TestUserRegister(BaseTestCase):

    @staticmethod
    def get_register_data():
        registration_data = {
            "first_name": "Alex",
            "last_name": "Shpak",
            "phone": "996772772772",
            "password": "super_secret_password",
            "locale": LocaleEnum.russian,
            "email": "test@example.com",
        }
        return ProfileRegister(**registration_data)

    @pytest.mark.asyncio
    async def test_user_registered_success(self):
        user_data = self.get_register_data()
        registered_user_id = await services.profile.register_user(
            self.db, user_data
        )
        user = await services.profile.get_by_phone(self.db, user_data.phone)
        assert user.id == registered_user_id

    @pytest.mark.asyncio
    async def test_user_register_phone_occupied(self):
        user_data = self.get_register_data()
        await ProfileFactory(phone=user_data.phone)
        with pytest.raises(HTTPException) as err:
            await services.profile.register_user(
                self.db, user_data
            )
        assert err.value.detail == "These credentials are already occupied!"

    @pytest.mark.asyncio
    async def test_user_register_email_occupied(self):
        user_data = self.get_register_data()
        await ProfileFactory(email=user_data.email)
        with pytest.raises(HTTPException) as err:
            await services.profile.register_user(
                self.db, user_data
            )
        assert err.value.detail == "This email is already in use!"
