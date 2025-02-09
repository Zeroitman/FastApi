from typing import Dict, Optional
import requests
from pydantic import constr
from requests.adapters import HTTPAdapter, Response
from starlette import status


class APIWrapper:
    url = None
    retry_max = 1
    hmac_key = None
    hmac_message = None

    def __init__(self):
        self.client = requests.Session()
        self.client.mount("http://", HTTPAdapter(max_retries=self.retry_max))
        self.client.mount("https://", HTTPAdapter(max_retries=self.retry_max))

    def get(
            self,
            path: constr(pattern=r'(^|)\/\w+'),  # noqa: F722
            params: Dict = None,
            headers: Dict = None
    ) -> Optional[Response]:
        uri_path = self.url + path
        try:
            response = self.client.get(
                uri_path, params=params, headers=headers
            )
            if response.status_code != status.HTTP_200_OK:
                return None
            return response
        except requests.RequestException as e:
            print("Error %s" % e)
            return None

    async def get_authenticated(
        self, path, locale: str = "ru", params: Dict = None
    ):
        headers = {
            "Accept-Language": locale
        }
        response = self.get(path, params=params, headers=headers)
        return response.json() if response \
            and response.status_code == status.HTTP_200_OK else None

    @staticmethod
    def get_empty_paginated_result(params: Dict):
        return {
            'page': params.get("page"),
            'size': params.get("size"),
            'pages': 0,
            'total': 0,
            "items": [],
        }

    async def get_paginated_data_or_empty_values(
            self, path, locale: str = "ru", params: Dict = None
    ) -> Dict:
        data = await self.get_authenticated(path, locale, params)
        return data if data else self.get_empty_paginated_result(params)
