import hashlib
import hmac
from datetime import datetime, timedelta
import pytest
from backend.authentication import generate_token
from backend.config import settings
from backend.db.models import Profile


async def get_access_token_for_user(profile: Profile):
    access_token, _ = await generate_token(
        data={"sub": profile.phone, "type": "access"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        type='access'
    )
    return access_token


def get_hmac_hash_for_date(today: datetime) -> str:
    hmac_hash = hmac.new(
        bytes(settings.USER_CONN.KEY, encoding='utf8'),
        str.encode(settings.USER_CONN.MESSAGE + today.now().date().strftime('%Y-%m-%d')),
        hashlib.sha256
    ).hexdigest()
    return hmac_hash


@pytest.mark.usefixtures("class_db", "client", "base_url", "test_db", "clear_tables")
class BaseTestCase:

    @staticmethod
    def _get_fields_for_pagination():
        return ["items", "page", "size", "pages", "total"]
