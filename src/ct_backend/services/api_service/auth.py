from pydantic import EmailStr

from ct_backend.database.repositories import user_repo
from ct_backend.core.security import token_service
from . import errors_schemas


async def process_register_user(username: str, email: EmailStr, role: str, password: str):
    if await user_repo.get_by_email(email):
        raise errors_schemas.ConflictError('User with this email already exists')

    # TODO: Отправка сообщения на email для подтверждения почты

    hashed_password = token_service.get_password_hash(password)

    user_id = user_repo.create(dict(
        username=username,
        email=email,
        role=role,
        hashed_password=hashed_password)
    )
    return {'user_id': user_id}
