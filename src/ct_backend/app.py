from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from ct_backend.services import APIError

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


@app.exception_handler(APIError)
async def app_error_handler(request: Request, exc: APIError):
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


app.include_router(current_router)
