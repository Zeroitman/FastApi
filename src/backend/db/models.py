import enum
from sqlalchemy import (
    Column, String, BigInteger, DateTime, func, text
)
from sqlalchemy.dialects.postgresql import ENUM
from backend.db.database import Base
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(Base, AsyncAttrs):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)


class LocaleEnum(str, enum.Enum):
    kyrgyz = 'ky'
    russian = 'ru'
    english = 'en'


class Profile(BaseModel):
    __tablename__ = 'profile'

    # authentication fields
    phone = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # personal data
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(80), nullable=True, unique=True)
    locale = Column(ENUM(LocaleEnum), nullable=True)

    # dates and time
    registered_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_on = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=func.now(), nullable=False)
