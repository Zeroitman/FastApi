import pytest
import pytest_asyncio
import httpx
from fastapi.testclient import TestClient
from backend.main import get_app

app = get_app()


@pytest.fixture(scope='session')
def base_url():
    yield TestClient(app).base_url


@pytest_asyncio.fixture(scope="function")
async def client():

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as c:
        yield c
