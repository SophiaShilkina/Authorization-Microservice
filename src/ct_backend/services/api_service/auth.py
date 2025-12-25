from pydantic import EmailStr

from ct_backend.database.repositories import user_repo


async def process_register_user(email: EmailStr):
    if await user_repo.get_by_email(email):
        raise
    # 1. Проверка, что email не занят
    # 2. Хэширование пароля
    # 3. Создание записи в БД с is_organization=False
    # 4. Отправка email для верификации (если нужно)
    # 5. Возвращаем созданного пользователя
    pass
