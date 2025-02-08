from fastapi import APIRouter
from backend.views import authentication


api_router = APIRouter()
api_router.include_router(authentication.auth_routes, tags=["Authentication"])


def init_app(app):
    app.include_router(api_router, prefix='/api')
