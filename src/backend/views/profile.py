from sqlalchemy.ext.asyncio import AsyncSession
from backend.authentication.token import check_access_token
from backend.db.database import get_db
from fastapi import APIRouter, Depends, Response
from starlette import status
from backend import services
from backend.db.models import Profile

profile_router = APIRouter()


@profile_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {"detail": "Activity not found"}
                }
            },
        }
    },
    description="Delete a user profile."
)
async def delete_profile(
        profile: Profile = Depends(check_access_token),
        db: AsyncSession = Depends(get_db),
):
    await services.profile.remove(db, id=profile.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
