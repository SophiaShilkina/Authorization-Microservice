from fastapi import APIRouter, Request, Response
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from ... import schemas
from auth_service.application.use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    LogoutAllUserUseCase
)
from auth_service.application.dto import (
    ContextDTO,
    LoginUserCommand,
    RegisterUserCommand,
    RefreshTokenCommand,
    LogoutUserCommand,
    LogoutAllUserCommand
)
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


@router.post('/refresh',
             response_model=schemas.ResponseEnvelope[schemas.RefreshResponse],
             responses={
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def refresh_token(
        body: schemas.RefreshRequest,
        uc: FromDishka[RefreshTokenUseCase],
):
    cmd = RefreshTokenCommand(
        refresh_token=str(body.refresh_token),
    )

    result = await uc.execute(cmd)

    return {
        'status': 'OK',
        'data': {
            'access_token': result.access_token,
            'refresh_token': result.refresh_token,
            'expires_at': result.expires_at,
        }
    }



@router.post('/logout',
             response_model=schemas.ResponseEnvelope[schemas.LogoutResponse],
             responses={
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def logout_user(
        body: schemas.LogoutRequest,
        uc: FromDishka[LogoutUserUseCase],
):
    cmd = LogoutUserCommand(
        refresh_token=str(body.refresh_token),
    )

    await uc.execute(cmd)

    return {
        'status': 'OK',
        'data': None
    }


@router.post('/logout-all',
             response_model=schemas.ResponseEnvelope[schemas.LogoutAllResponse],
             responses={
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def logout_all_user(
        body: schemas.LogoutAllRequest,
        uc: FromDishka[LogoutAllUserUseCase],
):
    cmd = LogoutAllUserCommand(
        access_token=body.access_token,
        access_token_expires_at=body.access_token_expires_at,
    )

    result = await uc.execute(cmd)

    return {
        'status': 'OK',
        'data': {
            'revoked_sessions': result.revoked_sessions,
        }
    }
