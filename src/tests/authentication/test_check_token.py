from datetime import timedelta
from unittest import mock

import pytest
from fastapi import HTTPException
from jwt import PyJWTError
from tests.base import BaseTestCase

from backend.authentication import generate_token
from backend.authentication.token import check_token
from backend.config import settings
from tests.factories import ProfileFactory


class TestUserToken(BaseTestCase):

    @pytest.mark.asyncio
    async def test_check_access_token_user_returned(self):
        redisClient = mock.MagicMock()
        expected_profile = await ProfileFactory()

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token, _ = await generate_token(
            data={"sub": expected_profile.phone, "type": "access"},
            expires_delta=access_token_expires,
            type='access'
        )

        returned_profile = await check_token(
            'access', access_token, self.db, redisClient
        )
        assert expected_profile.id == returned_profile.id
        assert redisClient.call_count == 0

    @pytest.mark.asyncio
    @mock.patch('jwt.decode')
    async def test_jwt_decode_error(
            self, mocked_decoder
    ):
        mocked_decoder.side_effect = PyJWTError()

        redisClient = mock.MagicMock()
        expected_profile = await ProfileFactory()

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token, _ = await generate_token(
            data={"sub": expected_profile.phone, "type": "access"},
            expires_delta=access_token_expires,
            type='access'
        )
        with pytest.raises(HTTPException):
            await check_token(
                'access', access_token, self.db, redisClient
            )

        assert redisClient.call_count == 0

    @pytest.mark.asyncio
    async def test_user_was_not_found(self):
        redisClient = mock.MagicMock()

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token, _ = await generate_token(
            data={"sub": '+996772686868', "type": "access"},
            expires_delta=access_token_expires,
            type='access'
        )
        with pytest.raises(HTTPException):
            await check_token(
                'access', access_token, self.db, redisClient
            )

        assert redisClient.call_count == 0
