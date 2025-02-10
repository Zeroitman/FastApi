from typing import List
from .base import PaginationResponseSchema
from pydantic import BaseModel, AnyHttpUrl, AnyUrl


class BannerBaseSchema(BaseModel):
    id: int
    image: AnyHttpUrl
    source: AnyUrl | None = None


class BannerPaginatedDisplaySchema(PaginationResponseSchema):
    items: List[BannerBaseSchema]
