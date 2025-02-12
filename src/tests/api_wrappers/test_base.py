import requests
import responses

from backend.api_wrappers.base import APIWrapper


class TestAPIWrapper:
    @responses.activate
    def test_get_success_without_query(self):
        wrapper = APIWrapper()
        wrapper.url = "https://someaddress.com"
        responses.add(
            responses.GET,
            f"{wrapper.url}/path/to/nowhere",
            json=["Hello"],
            status=200,
        )

        actual_response = wrapper.get("/path/to/nowhere",)
        assert actual_response.json() == ["Hello"]

    @responses.activate
    def test_get_success_with_query(self):
        wrapper = APIWrapper()
        wrapper.url = "https://someaddress.com"

        params = {
            "name": "John", "last_name": "Doe"
        }
        responses.add(
            responses.GET,
            f"{wrapper.url}/path/to/nowhere",
            json=["Hello"],
            status=200,
            match=[responses.matchers.query_param_matcher(params)]
        )

        actual_response = wrapper.get("/path/to/nowhere", params=params)
        assert actual_response.json() == ["Hello"]

    @responses.activate
    def test_get_wrong_code(self):
        wrapper = APIWrapper()
        wrapper.url = "https://someaddress.com"

        params = {
            "name": "John", "last_name": "Doe"
        }
        responses.add(
            responses.GET,
            f"{wrapper.url}/path/to/nowhere",
            status=303,
            match=[responses.matchers.query_param_matcher(params)]
        )

        actual_response = wrapper.get("/path/to/nowhere", params=params)
        assert actual_response is None

    @responses.activate
    def test_get_exception_raised(self):
        wrapper = APIWrapper()
        wrapper.url = "https://someaddress.com"

        params = {
            "name": "John", "last_name": "Doe"
        }
        responses.add(
            responses.GET,
            f"{wrapper.url}/path/to/nowhere",
            match=[responses.matchers.query_param_matcher(params)],
            body=requests.ConnectionError()
        )

        actual_response = wrapper.get("/path/to/nowhere", params=params)
        assert actual_response is None
