from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ct_backend.api.schemas import main_schemas
from ct_backend.services.api_service import auth as auth_service

router = APIRouter()


@router.post('/register', response_model=main_schemas.UserResponse)
async def register_user(body: main_schemas.UserCreate):
    await auth_service.process_register_user(body.email)

    return JSONResponse(
        status_code=200,
        content={"status": "OK"}
    )


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Используем стандартную форму OAuth2 для совместимости
    """
    # 1. Найти пользователя по email (form_data.username)
    # 2. Проверить пароль
    # 3. Проверить is_active
    # 4. Сгенерировать access и refresh токены
    # 5. Вернуть токены и данные пользователя
    pass


@router.post('/refresh')
async def refresh_token(refresh_token: str):
    """
    Получение нового access токена по refresh токену
    """
    # 1. Верифицировать refresh токен
    # 2. Извлечь user_id
    # 3. Сгенерировать новый access токен
    # 4. Вернуть новый access токен
    pass
