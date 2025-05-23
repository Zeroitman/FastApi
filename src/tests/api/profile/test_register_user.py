from unittest import mock
from httpx import AsyncClient
import pytest
from tests.base import BaseTestCase
from tests.factories import ProfileFactory
from backend.db.models import LocaleEnum


class TestRegisterUserView(BaseTestCase):

    @pytest.mark.asyncio
    async def test_register_user_successfully(
            self, client: AsyncClient, base_url
    ):
        response = await client.post(
            f'{base_url}/api/register/',
            json={
                "first_name": "John",
                "last_name": "Dho",
                "phone": "996772772772",
                "password": "super_secret_password",
                "code": "some_nice_otp_code",
                "email": "some@test.com",
                "locale": LocaleEnum.english
            }
        )
        assert response.status_code == 201
        assert 'id' in response.json()

    @pytest.mark.asyncio
    async def test_register_user_phone_is_occupied(
            self, client: AsyncClient, base_url
    ):
        profile = await ProfileFactory()
        response = await client.post(
            f'{base_url}/api/register/',
            json={
                "first_name": "John",
                "last_name": "Dho",
                "phone": profile.phone,
                "password": "super_secret_password",
                "code": "some_nice_otp_code",
                "locale": LocaleEnum.russian
            }
        )
        assert response.status_code == 400
        assert 'detail' in response.json()

    @pytest.mark.asyncio
    async def test_register_user_wrong_phone_prefix(
            self, client: AsyncClient, base_url
    ):
        response = await client.post(
            f'{base_url}/api/register/',
            json={
                "first_name": "John",
                "last_name": "Dho",
                "phone": "100200300",
                "password": "super_secret_password",
                "locale": LocaleEnum.english
            }
        )
        assert response.status_code == 422
