from datetime import timedelta, datetime
import pytest
import jwt
from freezegun import freeze_time
from backend.authentication import generate_token
from backend.config import settings


@pytest.mark.asyncio
@freeze_time('2022-04-27 12:40:00')
async def test_generate_access_token():
    data = {
        "email": "this is a random set of data",
        "sub": "another random key with random data"
    }
    expected_timedelta = timedelta(minutes=15)

    token, _ = await generate_token(data, expected_timedelta, 'access')

    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    assert payload['email'] == data['email']
    assert payload['sub'] == data['sub']
    assert "exp" in payload

    expire = datetime.fromtimestamp(payload.get("exp"))
    assert expire == datetime.now() + expected_timedelta
