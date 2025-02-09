from fastapi import Query
from .base import BaseFilter
from backend.config import settings


class BannerFilter(BaseFilter):
    def __init__(
            self,
            page: int | None = Query(
                default=1,
                description="Page number"
            ),
            size: int | None = Query(
                default=settings.COUNT_PER_PAGE_DEFAULT,
                description="Page size"
            )
    ):
        self.page = page
        self.size = size
