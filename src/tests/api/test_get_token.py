import pytest
from httpx import AsyncClient
from tests.factories import ProfileFactory
from backend.authentication import hashed_password
from tests.base import BaseTestCase


class TestGetToken(BaseTestCase):

    @pytest.mark.asyncio
    async def test_get_token_pair_success(self, client: AsyncClient, base_url):
        password = "test_Password1234"
        profile = await ProfileFactory(
            password=hashed_password(password),
        )
        response = await client.post(
            f"{base_url}/api/token/",
            json={
                "phone": profile.phone,
                "password": password,
            }
        )
        assert response.status_code == 200
        expected_token_pair = response.json()
        assert expected_token_pair['access'] is not None

    @pytest.mark.asyncio
    async def test_token_user_not_found(self, client: AsyncClient, base_url):
        response = await client.post(
            f"{base_url}/api/token/",
            json={
                "phone": "+99677777777",
                "password": "test_Password1234",
            }
        )
        assert response.status_code == 401
