import secrets
from typing import Optional

from passlib.context import CryptContext

from root.domain.value_objects import PasswordHashVO
from root.application.ports import IPasswordHasher
from root.application.security.policies import PasswordPolicy

pwd_context = CryptContext(
    schemes=['argon2'],
    default='argon2',
    deprecated='auto',
    argon2__time_cost=2,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__salt_len=16,
    argon2__hash_len=32,
)


class ArgonPasswordHasher(IPasswordHasher):
    _dummy_hash: Optional[str] = None

    def __init__(self):
        self._generate_dummy_hash()

    @staticmethod
    def get_password_hash(password: PasswordPolicy) -> PasswordHashVO:
        return PasswordHashVO(pwd_context.hash(password.value))

    @staticmethod
    def verify(plain_password: PasswordPolicy, hashed_password: PasswordHashVO) -> bool:
        return pwd_context.verify(plain_password.value, hashed_password.value)

    def dummy_verify(self, plain_password: PasswordPolicy) -> None:
        pwd_context.verify(plain_password.value, self._dummy_hash)

    def _generate_dummy_hash(self) -> None:
        self._dummy_hash = pwd_context.hash(secrets.token_urlsafe(32))
