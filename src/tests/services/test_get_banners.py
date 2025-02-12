import requests
import pytest
import responses
from tests.base import BaseTestCase
from tests.factories import BannerFactory
from backend.config import settings
from backend.db.schemas.banner import BannerPaginatedDisplaySchema
from backend import services


class TestBannerServiceGetBanners(BaseTestCase):

    @staticmethod
    def _generate_banners(count):
        banners = []
        for i in range(count):
            banners.append(BannerFactory().model_dump())
        return banners

    @responses.activate
    @pytest.mark.asyncio
    async def test_get_banners_from_api(self):
        params = {"page": 1, "size": 10}
        banner_data = self._generate_banners(10)
        banner_data = BannerPaginatedDisplaySchema(
            items=banner_data
        ).model_dump(mode="json")
        responses.add(
            responses.GET,
            settings.DRF_CONN.URL + "/api/banners/for-fa-project/",
            match=[responses.matchers.query_param_matcher(
                params, strict_match=False)],
            json=banner_data
        )
        actual_banners_data = await services.banners.get_banners(
            filter_schema=params, locale="ru"
        )
        assert len(actual_banners_data["items"]) == 10
        assert actual_banners_data == banner_data

    @responses.activate
    @pytest.mark.asyncio
    async def test_get_banners_from_api_connection_error(self):
        params = {"page": 1, "size": 10}
        responses.add(
            responses.GET,
            settings.DRF_CONN.URL + "/api/banners/for-fa-project/",
            match=[responses.matchers.query_param_matcher(
                params, strict_match=False)],
            body=requests.ConnectionError()
        )
        actual_banners_data = await services.banners.get_banners(
            filter_schema=params, locale="ru"
        )
        assert len(actual_banners_data["items"]) == 0
        assert "page" in actual_banners_data
        assert "size" in actual_banners_data
        assert "pages" in actual_banners_data
        assert "total" in actual_banners_data
