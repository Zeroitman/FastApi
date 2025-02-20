import pytest
from tests.base import BaseTestCase
from tests.factories import ProfileFactory
from backend.authentication import hashed_password
from backend import services


class TestAuthenticateUserProfileService(BaseTestCase):

    PASSWORD = 'secret_password'

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        profile = await ProfileFactory(password=hashed_password(self.PASSWORD))
        user = await services.profile.authenticate_user(
            self.db, profile.phone, self.PASSWORD
        )
        assert user

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self):
        profile = await ProfileFactory()
        user = await services.profile.authenticate_user(
            self.db, profile.phone, 'wrong_password'
        )
        assert not user

    @pytest.mark.asyncio
    async def test_authenticate_user_not_exists(self):
        user = await services.profile.authenticate_user(
            self.db, '996996996', self.PASSWORD
        )
        assert not user
