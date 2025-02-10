from typing import Dict
from .base import APIWrapper


class DrfProjectBackendAPIWrapper(APIWrapper):
    url = "http://drf-project:6197"
    PREFIX = "/api/"
    BANNERS_PATH = f"{PREFIX}banners/for-fa-project/"

    async def get_banners(self, params: Dict, locale: str):
        return await self.get_paginated_data_or_empty_values(
            path=self.BANNERS_PATH, locale=locale, params=params
        )


drf_project_api = DrfProjectBackendAPIWrapper()
