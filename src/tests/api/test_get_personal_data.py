import pytest
import json
from backend.db.schemas.profile import ProfileSchema
from backend.db.models import LocaleEnum
from tests.base import BaseTestCase, get_access_token_for_user
from tests.factories import ProfileFactory


class TestGetPersonalData(BaseTestCase):

    @pytest.mark.asyncio
    async def test_get_personal_data_success(
            self, client, base_url
    ):
        profile = await ProfileFactory(locale=LocaleEnum.russian)
        token = await get_access_token_for_user(profile)

        response = await client.get(
            f"{base_url}/api/profile/data/",
            headers={"Authorization": f"bearer {token}"},
        )
        expected_data = ProfileSchema.model_validate(profile)

        assert response.status_code == 200
        assert json.loads(expected_data.model_dump_json()) == response.json()
