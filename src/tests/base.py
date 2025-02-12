import pytest


@pytest.mark.usefixtures("client", "base_url")
class BaseTestCase:

    @staticmethod
    def _get_fields_for_pagination():
        return ["items", "page", "size", "pages", "total"]
