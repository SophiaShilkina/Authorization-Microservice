import secrets
from typing import Optional

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__salt_len=16,
    argon2__hash_len=32,
)


class PasswordHasher:
    _dummy_password: str = secrets.token_urlsafe(32)
    dummy_hash: Optional[str] = None

    def __init__(self):
        self._generate_dummy_hash()

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширование пароля"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return pwd_context.verify(plain_password, hashed_password)

    def _generate_dummy_hash(self) -> None:
        """Генерация фиктивного хеша один раз при старте"""
        self.dummy_hash = pwd_context.hash(self._dummy_password)


password_hasher = PasswordHasher()
