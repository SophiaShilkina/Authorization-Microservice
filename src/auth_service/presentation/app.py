from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from dishka.integrations.fastapi import setup_dishka

from .middleware import middleware
from .api import current_router
from .exception_handlers import register_exception_handlers
from auth_service.infrastructure.di import create_container


def create_app() -> FastAPI:
    app = FastAPI(
        title='Authorization microservice',
        description='API для взаимодействия с микросервисом авторизации, аутентификации и регистрации.',
        version='1.0.0',
        default_response_class=ORJSONResponse,
        middleware=middleware,
    )
    container = create_container()
    setup_dishka(container, app)

    app.include_router(current_router)

    register_exception_handlers(app)

    return app
