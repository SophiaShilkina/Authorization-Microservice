from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from ct_backend.api import current_router


middleware = [
    Middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['Content-Type']
    )
]

app = FastAPI(
    title="CaringTails Backend API",
    description="API для взаимодействия с бэкендом CaringTails.",
    version="1.0.0",
    middleware=middleware,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
    }
)

app.include_router(current_router)
