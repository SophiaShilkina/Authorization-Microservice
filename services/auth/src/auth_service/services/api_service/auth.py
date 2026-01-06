from typing import Any
from datetime import datetime

from pydantic import EmailStr, SecretStr

from auth_service.database.repositories import user_repo, refresh_token_repo
from auth_service.core.security import password_hasher, jwt_service, random_token_service
from auth_service.utils import extract_device_info, extract_ip_address
from . import errors_schemas


async def process_register_user(email: EmailStr, role: str, password: SecretStr) -> dict[str, Any]:
    """
    Регистрация пользователя
    1. Проверка не занят ли email
    2. Хэширование пароля
    3. Создание пользователя в БД
    4. Возврат словаря
    """

    if await user_repo.get_id_by_email(email):
        raise errors_schemas.ConflictError('User with this email already exists')

    hashed_password = password_hasher.get_password_hash(password.get_secret_value())

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

    # TODO: Отправка сообщения на email для подтверждения почты


async def process_login_user(request_context: dict[str, Any], email: EmailStr, password: SecretStr) -> dict[str, Any]:
    user = await user_repo.get_by_email(email)
    plain_password = password.get_secret_value()

    if not user:
        password_hasher.verify_password(plain_password, password_hasher.dummy_hash)
        raise errors_schemas.UnauthorizedError("Invalid email or password")

    if not password_hasher.verify_password(plain_password,user["hashed_password"]):
        raise errors_schemas.UnauthorizedError("Invalid email or password")

    if not user["is_active"] or user["is_blocked"]:
        raise errors_schemas.ForbiddenError('The user account is blocked or disabled')

    if not user["is_verified"]:
        raise errors_schemas.ForbiddenError('The account has not been verified')

    access_token = jwt_service.create_access_token({
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
    })

    refresh_token = random_token_service.create_refresh_token()
    refresh_token_hash = random_token_service.hash_token(refresh_token)

    await refresh_token_repo.create({
        'user_id': user["id"],
        'token_hash': refresh_token_hash,
        'expires_at': datetime.now() + random_token_service.refresh_token_expire_days,
        'last_used_at': datetime.now(),
        "device_info": extract_device_info(request_context),
        "ip_address": extract_ip_address(request_context),
        })

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
