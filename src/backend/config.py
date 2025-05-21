import os
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceConnParams(BaseModel):
    KEY: str = "default_key"
    MESSAGE: str = "default_message"
    URL: str = "http://drf-project:6197"


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Fast Api Project'
    COUNT_PER_PAGE_DEFAULT: int = 10
    JWT_SECRET_KEY: str = Field(
        default='a94f6b2d7e183c5a9c12e847d9',
        json_schema_extra={'env': 'SECRET_KEY'}
    )
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        json_schema_extra={'env': 'ACCESS_TOKEN_EXPIRE_MINUTES'}
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        default=1440,
        json_schema_extra={'env': 'REFRESH_TOKEN_EXPIRE_MINUTES'}
    )
    # DATABASE CONNECTION PARAMS
    CONNECTION_POOL: int = Field(
        default=5, json_schema_extra={'env': 'CONNECTION_POOL'}
    )
    MAX_OVERFLOW: int = Field(
        default=10,
        json_schema_extra={'env': 'MAX_OVERFLOW'}
    )
    POOL_RECYCLE: int = Field(
        default=3600,
        json_schema_extra={'env': 'POOL_RECYCLE'}
    )
    POSTGRES_HOST: str = Field(..., json_schema_extra={'env': 'POSTGRES_HOST'})
    POSTGRES_PORT: int = Field(..., json_schema_extra={'env': 'POSTGRES_PORT'})
    DATABASE_NAME: str = Field(..., json_schema_extra={'env': 'DATABASE_NAME'})
    POSTGRES_USER: str = Field(..., json_schema_extra={'env': 'POSTGRES_USER'})
    POSTGRES_PASSWORD: str = Field(
        ..., json_schema_extra={'env': 'POSTGRES_PASSWORD'}
    )

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", ".env")
    )

    # HMAC authentication
    DRF_CONN: ServiceConnParams = ServiceConnParams()

settings = Settings()

def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.DATABASE_NAME}")
