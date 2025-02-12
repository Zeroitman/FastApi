from unittest import mock
import pytest
from backend.db.schemas.banner import BannerPaginatedDisplaySchema
from tests.factories import BannerFactory


class TestGetBannersAPIView:

    @staticmethod
    def _generate_banners(count):
        banners = []

        for _ in range(count):
            banners.append(BannerFactory().model_dump())

        return banners

    @mock.patch("backend.services.banners.get_banners")
    @pytest.mark.asyncio
    async def test_get_banners_success(
            self,
            mocked_services_layer,
            client, base_url
    ):
        banners = self._generate_banners(10)
        expected_banners = BannerPaginatedDisplaySchema(
            items=banners
        ).model_dump(mode='json')
        mocked_services_layer.return_value = expected_banners
        response = await client.get(
            f"{base_url}/api/banners/",
            headers={"Authorization": f"bearer du3hrukhf3u4h8tfi3bu"},
        )
        assert response.status_code == 200
        actual_data = response.json()
        expected_data = expected_banners
        assert actual_data == expected_data
