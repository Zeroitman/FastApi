from typing import Optional
from pydantic import (
    BaseModel,
    constr,
    Field,
    EmailStr,
    ConfigDict
)
from backend.db.models import LocaleEnum



class ProfileRegister(BaseModel):
    phone: constr(
        max_length=150,
        pattern=r'(?:^|\s)996\d*'
    )
    password: constr(max_length=80)

    email: EmailStr | None = None
    first_name: constr(
        min_length=1,
        max_length=150
    )
    last_name: constr(
        min_length=2,
        max_length=150
    )
    locale: LocaleEnum = Field(...,
        description="Preferred user's locale"
    )

class ProfileSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    phone: str
    email: Optional[EmailStr] = None
    first_name: str
    last_name: str
    locale: Optional[LocaleEnum]
