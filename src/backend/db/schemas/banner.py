from typing import List
from .base import PaginationResponseSchema
from pydantic import BaseModel, AnyHttpUrl, AnyUrl


class BannerBaseSchema(BaseModel):
    id: int
    image: AnyHttpUrl
    source: AnyUrl | None = None
    station_ids: List[int]


class BannerPaginatedDisplaySchema(PaginationResponseSchema):
    items: List[BannerBaseSchema]
