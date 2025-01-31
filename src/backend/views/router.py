from fastapi import APIRouter

api_router = APIRouter()


def init_app(app):
    app.include_router(api_router, prefix='/api')
