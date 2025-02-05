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
