import os
from typing import ClassVar
from pydantic import (
    AnyHttpUrl,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVER_NAME: str = Field(
        env='SERVER_NAME',
        default='development'
    )
    SERVER_HOST: AnyHttpUrl = "http://0.0.0.0"
    PROJECT_NAME: str = 'Fast Api Project'

    TIMEZONE: str = Field(
        env='TIMEZONE',
        default='Asia/Bishkek'
    )
    COUNT_PER_PAGE_DEFAULT: int = 10

    JWT_SECRET_KEY: str = Field(
        env='SECRET_KEY',
        default='a94f6b2d7e183c5a9c12e847d93056ef4b82d7c1f0a3658e5f1b3c29d6a7e'
    )
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        env='ACCESS_TOKEN_EXPIRE_MINUTES',
        default=30
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        env='REFRESH_TOKEN_EXPIRE_MINUTES',
        default=1440
    )

    DATE_INPUT_FORMAT: ClassVar[str] = "%Y-%m-%d"
    DATETIME_INPUT_FORMAT: ClassVar[str] = "%Y-%m-%dT%H:%M:%S%z"

    DATETIME_EXPORT_FORMAT: str = Field(
        env='DATETIME_EXPORT_FORMAT', default='%Y-%m-%dT%H:%M:%S%z'
    )

    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    POSTGRES_PORT: int = Field(..., env='POSTGRES_PORT')
    DATABASE_NAME: str = Field(..., env='DATABASE_NAME')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", ".env")
    )

settings = Settings()

def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.DATABASE_NAME}")
