from fastapi import APIRouter
from backend.views import authentication, profile


api_router = APIRouter()
api_router.include_router(authentication.auth_routes, tags=["Authentication"])
api_router.include_router(profile.profile_router, prefix='/profile', tags=["Profile"])


def init_app(app):
    app.include_router(api_router, prefix='/api')
