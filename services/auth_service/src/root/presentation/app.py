from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from dishka.integrations.fastapi import setup_dishka

from .middleware import create_middleware
from .api import current_router
from .exceptions import register_exception_handlers
from root.infrastructure.config import Config
from root.infrastructure.di import create_container


def create_app() -> FastAPI:
    config = Config.load()
    container = create_container(config)

    app = FastAPI(
        title='Authorization microservice',
        description='API для взаимодействия с микросервисом авторизации, аутентификации и регистрации.',
        version='1.0.0',
        default_response_class=ORJSONResponse,
        middleware=create_middleware(config),
    )

    setup_dishka(container, app)

    app.include_router(current_router)

    register_exception_handlers(app)

    return app
