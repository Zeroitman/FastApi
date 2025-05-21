import logging
from importlib.metadata import entry_points
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from backend.config import settings

logger = logging.getLogger('Fast-Api-Project')


def load_modules(app=None):
    for ep in entry_points().select(group="backend.modules"):
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                init_app(app)


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='development',
        version="1.0.0",
        description=f"OpenAPI Documentation of the {settings.PROJECT_NAME}",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema


def get_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="This is a backend server",
        version="1.0.0",
    )
    load_modules(app)
    custom_openapi(app)
    return app
