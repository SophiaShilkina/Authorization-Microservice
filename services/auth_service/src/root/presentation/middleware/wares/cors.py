from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from root.infrastructure.config import Config


def create_cors_middleware(config: Config) -> Middleware:
    return Middleware(
        CORSMiddleware,
        allow_origins=config.cors.allow_origins,
        allow_credentials=config.cors.allow_credentials,
        allow_methods=config.cors.allow_methods,
        allow_headers=config.cors.allow_headers,
    )
