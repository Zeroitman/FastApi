from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from fastapi import APIRouter, Depends, Response, Path, HTTPException
from starlette import status
from backend import services


profile_router = APIRouter()


@profile_router.delete(
    "/{id}/",
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
        id: int = Path(..., title="User ID"),
        db: AsyncSession = Depends(get_db),
):

    try:
        await services.profile.remove(db, id=id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="These credentials are already occupied!",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

