from backend.api_wrappers import drf_project_api
from backend.filters.base import BaseFilter


class BannerService:

    @staticmethod
    async def get_banners(filter_schema, locale):
        params = filter_schema
        if isinstance(filter_schema, BaseFilter):
            params = filter_schema.to_dict()
        return await drf_project_api.get_banners(params, locale)


banners = BannerService()
