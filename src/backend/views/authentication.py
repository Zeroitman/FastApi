from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from backend import services
from backend.db.database import get_db
from backend.db.schemas.profile import ProfileRegister
from passlib.context import CryptContext


# pwd_context stably generates hash of 60 symbols length with this config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password):
    return pwd_context.hash(password)


auth_routes = APIRouter()



@auth_routes.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {"id": 3456}
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "This credentials are already occupied!"}
                }
            },
        }
    },
    response_description='register user by phone and password'
)
async def register(
        registration_data: ProfileRegister,
        db: Session = Depends(get_db),
):
    registration_data.password = hashed_password(registration_data.password)

    profile_id = await services.profile.register_user(
        db, registration_data,
    )

    return {"id": profile_id}
