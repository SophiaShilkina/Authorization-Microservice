from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import fastapi_swagger_dark as fsd

from auth_service.database import engine_management
from auth_service.services import APIError
from auth_service.api import current_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    yield
    await engine_management.dispose()

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
    docs_url=None,
    title="CaringTails Backend API",
    description="API для взаимодействия с бэкендом CaringTails.",
    version="1.0.0",
    lifespan=lifespan,
    middleware=middleware,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "theme": "dark",
    }
)


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.error,
            "message": exc.message,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "Internal Server Error",
            "message": "Unexpected server error",
        },
    )

# TODO: убрать темную тему в проде
fsd.install(current_router, path="/docs")
app.include_router(current_router)
