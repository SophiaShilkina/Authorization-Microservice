from typing import Any

from pydantic import EmailStr, SecretStr

from auth_service.database.repositories import user_repo
from auth_service.core.security import token_service
from . import errors_schemas


async def process_register_user(email: EmailStr, role: str, password: SecretStr) -> dict[str, Any]:
    """
    Регистрация пользователя
    1. Проверка не занят ли email
    2. Хэширование пароля
    3. Создание пользователя в БД
    4. Возврат словаря
    """

    if await user_repo.get_by_email(email):
        raise errors_schemas.ConflictError('User with this email already exists')

    # TODO: Отправка сообщения на email для подтверждения почты

    hashed_password = token_service.get_password_hash(password.get_secret_value())

    user_id = await user_repo.create(dict(
        email=email,
        role=role,
        hashed_password=hashed_password
    ))

    return {
        'id': user_id,
        'email': email,
        'role': role
    }
