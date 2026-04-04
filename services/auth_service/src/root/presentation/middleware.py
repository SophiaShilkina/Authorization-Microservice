from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from root.infrastructure.config import Config

config = Config()

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['POST'],
        allow_headers=['*']
    )
]
