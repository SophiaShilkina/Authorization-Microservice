from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ct_backend.api.schemas import main_schemas
from ct_backend.api.schemas.errors import ErrorResponse
from ct_backend.services import auth

router = APIRouter()


@router.post('/register',
             response_model=main_schemas.UserResponse,
             responses={
                 409: {"model": ErrorResponse, "description": "User already exists"},
                 500: {"model": ErrorResponse},
             })
async def register_user(body: main_schemas.UserCreate):
    data = await auth.process_register_user(body.username, body.email, body.role, body.password)

    return JSONResponse(
        status_code=200,
        content={"status": "OK",
                 "data": data}
    )
#
#
# @router.post('/login', response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     """
#     Используем стандартную форму OAuth2 для совместимости
#     """
#     # 1. Найти пользователя по email (form_data.username)
#     # 2. Проверить пароль
#     # 3. Проверить is_active
#     # 4. Сгенерировать access и refresh токены
#     # 5. Вернуть токены и данные пользователя
#     pass
#
#
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
