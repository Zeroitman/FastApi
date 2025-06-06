from sqlalchemy.ext.asyncio import AsyncSession
from backend.authentication import check_access_token
from backend.db.database import get_db
from fastapi import APIRouter, Depends, Response, HTTPException
from starlette import status
from backend import services
from backend.db.models import Profile
from backend.db.schemas.profile import ProfileSchema, ProfileEditSchema

profile_router = APIRouter()


@profile_router.get(
    "/data/",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {"detail": "some detail"}
                }
            },
        }
    },
    response_model=ProfileSchema,
    response_description="Returns personal data"
)
async def get_profile_personal_data(
        profile: Profile = Depends(check_access_token),
):
    return profile


@profile_router.patch(
    "/data/",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {"detail": "some detail"}
                }
            },
        }
    },
    response_model=ProfileSchema,
    response_description="Edit personal data"
)
async def edit_profile_personal_data(
        profile_data: ProfileEditSchema,
        db: AsyncSession = Depends(get_db),
        profile: Profile = Depends(check_access_token),
):
    if profile_data.email:
        existed_profile = await services.profile.get_by_email(
            db, profile_data.email
        )
        if existed_profile and existed_profile.id != profile.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already in use!",
            )
    profile = await services.profile.update(
        db,
        exclude_fields={"registered_on", "updated_on"},
        db_obj=profile,
        obj_in=profile_data
    )
    return profile


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
