from fastapi import APIRouter, Request, Response

from auth_service.api import schemas
from auth_service.services import auth as auth_service
from auth_service.utils import get_request_context
from auth_service import config

router = APIRouter()


@router.post('/register',
             response_model=schemas.ResponseEnvelope[schemas.RegisterResponse],
             responses={
                 409: {"model": schemas.ErrorResponse, "description": "User already exists"},
                 500: {"model": schemas.ErrorResponse},
             })
async def register_user(body: schemas.RegisterRequest):
    data = await auth_service.process_register_user(
        body.email,
        body.role,
        body.password
    )
    return {
        "status": "OK",
        "data": data
    }


@router.post('/login',
             response_model=schemas.ResponseEnvelope[schemas.LoginResponse],
             responses={
                 401: {"model": schemas.ErrorResponse, "description": "Unauthorized"},
                 403: {"model": schemas.ErrorResponse, "description": "Forbidden"},
                 500: {"model": schemas.ErrorResponse},
             })
async def login_user(body: schemas.LoginRequest, request: Request, response: Response):
    request_context = get_request_context(request)

    data = await auth_service.process_login_user(
        request_context,
        body.email,
        body.password,
    )

    response.set_cookie(
        key=config.cookie.name,
        value=data['refresh_token'],
        httponly=config.cookie.httponly,
        secure=config.cookie.secure,
        samesite=config.cookie.samesite,
        max_age=config.cookie.max_age,
    )

    return {
        "status": "OK",
        "data": {
            'access_token': data['access_token']
        }
    }


# @router.post('/refresh')
# async def refresh_token(refresh_token: str):
#     """
#     Получение нового access токена по refresh токену
#     """
#     # 1. Верифицировать refresh токен
#     # 2. Извлечь user_id
#     # 3. Сгенерировать новый access токен
#     # 4. Вернуть новый access токен
#     pass
