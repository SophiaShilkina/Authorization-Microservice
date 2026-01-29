from fastapi import APIRouter, Request, Response
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from ... import schemas
from auth_service.application.use_cases import LoginUserUseCase, RegisterUserUseCase
from auth_service.application.dto import LoginUserCommand, ContextDTO, RegisterUserCommand
from auth_service.infrastructure import config

router = APIRouter()


@router.post('/register',
             response_model=schemas.ResponseEnvelope[schemas.RegisterResponse],
             responses={
                 409: {'model': schemas.ErrorResponse, 'description': 'Conflict'},
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def register_user(
        body: schemas.RegisterRequest,
        request: Request,
        uc: FromDishka[RegisterUserUseCase],
):
    cmd = RegisterUserCommand(
        email=str(body.email),
        username=body.username,
        password=str(body.password),
        context=ContextDTO(
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get('user-agent'),
        )
    )

    result = await uc.execute(cmd)

    return {
        'status': 'OK',
        'data': {
            'id': result.id,
            'email': result.email,
            'username': result.username,
        }
    }


@router.post('/login',
             response_model=schemas.ResponseEnvelope[schemas.LoginResponse],
             responses={
                 401: {'model': schemas.ErrorResponse, 'description': 'Unauthorized'},
                 403: {'model': schemas.ErrorResponse, 'description': 'Forbidden'},
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def login_user(
        body: schemas.LoginRequest,
        request: Request,
        response: Response,
        uc: FromDishka[LoginUserUseCase],
):
    cmd = LoginUserCommand(
        email=str(body.email),
        password=str(body.password),
        context=ContextDTO(
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get('user-agent'),
        )
    )

    result = await uc.execute(cmd)
    #
    # response.set_cookie(
    #     key=config.cookie.name,
    #     value=data['refresh_token'],
    #     httponly=config.cookie.httponly,
    #     secure=config.cookie.secure,
    #     samesite=config.cookie.samesite,
    #     max_age=config.cookie.max_age,
    # )

    return {
        'status': 'OK',
        'data': {
            'access_token': result.access_token,
            'refresh_token': result.refresh_token,
            'expires_at': result.expires_at,
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
