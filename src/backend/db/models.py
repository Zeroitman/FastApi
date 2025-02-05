from sqlalchemy import (
    Column, String, BigInteger, DateTime, func, text
)
from backend.db.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)


class Profile(BaseModel):
    __tablename__ = 'profile'

    # authentication fields
    phone = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # personal data
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(80), nullable=True, unique=True)

    # dates and time
    registered_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_on = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=func.now(), nullable=False)
