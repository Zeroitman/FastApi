import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.config import settings, get_db_url

DATABASE_URL = get_db_url()
async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.CONNECTION_POOL,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE
)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine
)

Base = declarative_base()


async def get_db():
    uri = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql')
    try:
        await asyncpg.connect(uri)
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            database='template1',
            user=settings.POSTGRES_USER,
            host=settings.POSTGRES_HOST,
            password=settings.POSTGRES_PASSWORD
        )
        await sys_conn.execute(
            f'CREATE DATABASE {settings.DATABASE_NAME} OWNER {settings.POSTGRES_USER}'
        )
        await sys_conn.close()
    async with async_session() as session:
        yield session
