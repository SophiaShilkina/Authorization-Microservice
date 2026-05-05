from starlette.middleware import Middleware

from root.infrastructure.config import Config

from .wares import create_cors_middleware


def create_middleware(config: Config) -> list[Middleware]:
    return [
        create_cors_middleware(config),
    ]
