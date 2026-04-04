from fastapi import APIRouter, Request, Response, Depends, HTTPException
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from ... import schemas
from root.application.use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    LogoutAllUserUseCase
)
from root.application.dto import (
    ContextDTO,
    LoginUserCommand,
    RegisterUserCommand,
    RefreshTokenCommand,
    LogoutUserCommand,
    LogoutAllUserCommand
)
from root.infrastructure.config import Config
from root.presentation.api.dependencies import get_bearer_token

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
        password=body.password.get_secret_value(),
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
        config: FromDishka[Config],
):
    cmd = LoginUserCommand(
        email=str(body.email),
        password=body.password.get_secret_value(),
        context=ContextDTO(
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get('user-agent'),
        )
    )

    result = await uc.execute(cmd)

    response.set_cookie(
        key=config.cookie.name,
        value=result.refresh_token,
        httponly=config.cookie.httponly,
        secure=config.cookie.secure,
        samesite=config.cookie.samesite,  # type: ignore
        max_age=config.cookie.max_age,
    )

    return {
        'status': 'OK',
        'data': {
            'access_token': result.access_token,
        }
    }


@router.post('/refresh',
             response_model=schemas.ResponseEnvelope[schemas.RefreshResponse],
             responses={
                 401: {'model': schemas.ErrorResponse, 'description': 'Unauthorized'},
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def refresh_token(
        request: Request,
        response: Response,
        uc: FromDishka[RefreshTokenUseCase],
        config: FromDishka[Config],
        access_token: str = Depends(get_bearer_token),
):
    refresh_token_value = request.cookies.get(config.cookie.name)

    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token required')

    cmd = RefreshTokenCommand(
        refresh_token=refresh_token_value,
        access_token=access_token,
    )

    result = await uc.execute(cmd)

    response.set_cookie(
        key=config.cookie.name,
        value=result.refresh_token,
        httponly=config.cookie.httponly,
        secure=config.cookie.secure,
        samesite=config.cookie.samesite,  # type: ignore
        max_age=config.cookie.max_age,
    )

    return {
        'status': 'OK',
        'data': {
            'access_token': result.access_token,
        }
    }


@router.post('/logout',
             response_model=schemas.ResponseEnvelope[None],  # type: ignore
             responses={
                 401: {'model': schemas.ErrorResponse, 'description': 'Unauthorized'},
                 500: {'model': schemas.ErrorResponse},
             })
@inject
async def logout_user(
        request: Request,
        response: Response,
        uc: FromDishka[LogoutUserUseCase],
        config: FromDishka[Config],
):
    refresh_token_value = request.cookies.get(config.cookie.name)

    if not refresh_token_value:
        raise HTTPException(status_code=401, detail='Refresh token required')

    cmd = LogoutUserCommand(
        refresh_token=refresh_token_value,
    )

    await uc.execute(cmd)

    response.delete_cookie(
        key=config.cookie.name,
    )

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
        response: Response,
        uc: FromDishka[LogoutAllUserUseCase],
        config: FromDishka[Config],
        access_token: str = Depends(get_bearer_token),
):
    cmd = LogoutAllUserCommand(
        access_token=access_token,
    )

    result = await uc.execute(cmd)

    response.delete_cookie(
        key=config.cookie.name,
    )

    return {
        'status': 'OK',
        'data': {
            'revoked_sessions': result.revoked_sessions,
        }
    }
