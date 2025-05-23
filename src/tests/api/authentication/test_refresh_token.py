from datetime import timedelta
from unittest import mock

import pytest
from freezegun import freeze_time
from tests.factories import ProfileFactory
from backend.authentication import generate_token
from backend.config import settings
from tests.base import BaseTestCase


class TestGetRefreshToken(BaseTestCase):

    @pytest.mark.asyncio
    @freeze_time('2025-04-27 11:00:00')
    @mock.patch('backend.views.authentication.check_refresh_token')
    @mock.patch(
        'backend.views.authentication.services.profile.update_refresh_token'
    )
    async def test_refresh_get_token_pair_success(
            self, mocked_update,
            mocked_checker, client,
            base_url
    ):
        profile = await ProfileFactory()

        refresh_token_expires = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        refresh_token, code = await generate_token(
            data={"sub": profile.email, "type": "refresh"},
            expires_delta=refresh_token_expires,
            type='refresh'
        )

        mocked_checker.return_value = profile

        response = await client.post(
            f"{base_url}/api/refresh/",
            json={
                "refresh": refresh_token
            }
        )
        mocked_checker.assert_called_once()

        assert response.status_code == 200

        expected_token_pair = response.json()
        assert expected_token_pair['access'] is not None
        assert expected_token_pair['refresh'] is not None

        mocked_update.assert_called_once()
