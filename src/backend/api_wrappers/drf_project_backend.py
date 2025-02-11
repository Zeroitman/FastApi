from typing import Dict
from backend.config import settings
from .base import APIWrapper


class DrfProjectBackendAPIWrapper(APIWrapper):
    hmac_key = settings.DRF_CONN.KEY
    hmac_message = settings.DRF_CONN.MESSAGE
    url = "http://drf-project:6197"
    PREFIX = "/api/"
    BANNERS_PATH = f"{PREFIX}banners/for-fa-project/"

    async def get_banners(self, params: Dict, locale: str):
        return await self.get_paginated_data_or_empty_values(
            path=self.BANNERS_PATH, locale=locale, params=params
        )


drf_project_api = DrfProjectBackendAPIWrapper()
