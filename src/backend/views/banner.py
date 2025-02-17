from fastapi import APIRouter, Depends
from backend.db.models import Profile
from backend.db.schemas.banner import BannerPaginatedDisplaySchema
from backend import services
from backend.filters.banner import BannerFilter
from backend.authentication import check_access_token

banner_router = APIRouter()


@banner_router.get(
    "/",
    response_model=BannerPaginatedDisplaySchema,
    response_description='Returns banners list',
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {"detail": "some detail"}
                }
            },
        },
    },
)
async def get_banners(
        profile: Profile = Depends(check_access_token),
        filter_schema: BannerFilter = Depends(),
):
    return await services.banners.get_banners(
        filter_schema, profile.locale
    )
