from unittest import mock
import pytest
from tests.base import BaseTestCase, get_access_token_for_user
from backend.db.schemas.banner import BannerPaginatedDisplaySchema
from tests.factories import BannerFactory, ProfileFactory


class TestGetBannersAPIView(BaseTestCase):

    @staticmethod
    def _generate_banners(count):
        banners = []

        for _ in range(count):
            banners.append(BannerFactory().model_dump())

        return banners

    @mock.patch("backend.services.banners.get_banners")
    @pytest.mark.asyncio
    async def test_get_banners_success_token_provided(
            self,
            mocked_services_layer,
            client, base_url
    ):
        profile = await ProfileFactory()
        token = await get_access_token_for_user(profile)
        banners = self._generate_banners(10)
        expected_banners = BannerPaginatedDisplaySchema(
            items=banners
        ).model_dump(mode='json')
        mocked_services_layer.return_value = expected_banners
        response = await client.get(
            f"{base_url}/api/banners/",
            headers={"Authorization": f"bearer {token}"},
        )
        assert response.status_code == 200
        actual_data = response.json()
        expected_data = expected_banners
        assert actual_data == expected_data
