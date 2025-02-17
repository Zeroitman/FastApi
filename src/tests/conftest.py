import asyncio
from unittest import mock

import asyncpg
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from async_asgi_testclient import TestClient as ASGITestClient
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession
)
from backend.config import settings
from backend.db.database import Base
from backend.db.database import async_engine as main_engine
from backend.db.database import get_db
from backend.main import get_app
from sqlalchemy.orm import scoped_session, sessionmaker


async def setup_database(database_uri: str):
    uri = database_uri.replace('postgresql+asyncpg', 'postgresql')
    try:
        conn = await asyncpg.connect(uri)
        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            database='template1',
            user=settings.POSTGRES_USER,
            host=settings.POSTGRES_HOST,
            password=settings.POSTGRES_PASSWORD
        )
        await sys_conn.execute(
            f'CREATE DATABASE {settings.DATABASE_NAME}_test OWNER {settings.POSTGRES_USER}'
        )
        await sys_conn.close()

if not settings.TESTING:
    TEST_DATABASE_URI = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.DATABASE_NAME}_test"
    engine = create_async_engine(TEST_DATABASE_URI)
    asyncio.run(setup_database(TEST_DATABASE_URI))
else:
    engine = main_engine


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
TestSessionLocal = scoped_session(async_session)


async def override_get_db():
    async with async_session() as session:
        yield session
        await session.commit()


app = get_app()
app.jetstream = mock.AsyncMock()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='class')
async def class_db(request):
    async with async_session() as session:
        request.cls.db = session
        yield session

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
            await session.commit()


@pytest_asyncio.fixture(scope='function')
async def clear_tables():
    async with async_session() as session:
        yield session
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
            await session.commit()


@pytest_asyncio.fixture(scope='session')
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def base_url():
    yield TestClient(app).base_url


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncClient:

    async with AsyncClient(app=app) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def async_client():

    async with ASGITestClient(application=app) as c:
        yield c
