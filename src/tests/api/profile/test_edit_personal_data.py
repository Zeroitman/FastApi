import pytest
from tests.base import BaseTestCase, get_access_token_for_user
from tests.factories import ProfileFactory
from backend.db.models import LocaleEnum


class TestEditPersonalDataView(BaseTestCase):

    @staticmethod
    def get_data_for_update(email: str = "test@email.com"):
        return {
            "first_name": "Some name",
            "last_name": "Some last name",
            "email": email,
            "locale": LocaleEnum.russian.value
        }

    @pytest.mark.asyncio
    async def test_edit_personal_data_success(
            self,
            client,
            base_url
    ):
        updated_data = self.get_data_for_update()
        profile = await ProfileFactory(email="test@test.com")
        token = await get_access_token_for_user(profile)

        response = await client.patch(
            f"{base_url}/api/profile/data/",
            headers={"Authorization": f"bearer {token}"},
            json=updated_data
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_edit_personal_data_email_in_use(
            self,
            client,
            base_url
    ):
        await ProfileFactory(email="test@email.com")
        updated_data = self.get_data_for_update()
        profile = await ProfileFactory(email="test@test.com")
        token = await get_access_token_for_user(profile)
        response = await client.patch(
            f"{base_url}/api/profile/data/",
            headers={"Authorization": f"bearer {token}"},
            json=updated_data
        )
        assert response.status_code == 400
        assert response.json()['detail'] == 'Email is already in use!'

    @pytest.mark.asyncio
    async def test_edit_personal_data_email_belongs_to_user(
            self,
            client,
            base_url
    ):
        updated_data = self.get_data_for_update()
        profile = await ProfileFactory(email="test@email.com")
        token = await get_access_token_for_user(profile)
        response = await client.patch(
            f"{base_url}/api/profile/data/",
            headers={"Authorization": f"bearer {token}"},
            json=updated_data
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_edit_personal_data_email_not_provided(
            self,
            client,
            base_url
    ):
        updated_data = self.get_data_for_update()
        updated_data.pop("email")
        await ProfileFactory(email=None)
        profile = await ProfileFactory(email=None)
        token = await get_access_token_for_user(profile)
        response = await client.patch(
            f"{base_url}/api/profile/data/",
            headers={"Authorization": f"bearer {token}"},
            json=updated_data
        )
        assert response.status_code == 200
