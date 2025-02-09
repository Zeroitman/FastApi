from pydantic import BaseModel
from backend.config import settings


class PaginationResponseSchema(BaseModel):
    page: int | None = 1
    size: int | None = settings.COUNT_PER_PAGE_DEFAULT
    pages: int | None = 0
    total: int | None = 0
