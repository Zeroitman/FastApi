import pytest
from tests.base import BaseTestCase, get_access_token_for_user
from tests.factories import ProfileFactory


class TestRemoveProfileApiView(BaseTestCase):

    @pytest.mark.asyncio
    async def test_remove_profile_successful(self, base_url, client):
        profile = await ProfileFactory()
        token = await get_access_token_for_user(profile)
        response = await client.delete(
            f'{base_url}/api/profile/',
            headers={"Authorization": f"bearer {token}"},
        )
        assert response.status_code == 204
