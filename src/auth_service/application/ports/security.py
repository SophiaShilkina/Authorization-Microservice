from typing import Protocol
from datetime import datetime

from auth_service.domain.value_objects import TokenVO, TokenHashVO, PasswordHashVO
from ..security.policies import PasswordPolicy
from ..security.models import AccessTokenPayload


class IPasswordHasher(Protocol):
    """Interface (port) for password hashing service"""

    @staticmethod
    def get_password_hash(password: PasswordPolicy) -> PasswordHashVO: ...

    @staticmethod
    def verify(plain_password: PasswordPolicy, password_hash: PasswordHashVO) -> bool: ...

    def dummy_verify(self, plain_password: PasswordPolicy) -> None: ...


class IRefreshTokenService(Protocol):
    """Interface (port) for refresh token service"""

    def generate(self) -> tuple[TokenVO, TokenHashVO]: ...

    @staticmethod
    def hash(raw_token: TokenVO) -> TokenHashVO: ...


class IAccessTokenService(Protocol):
    """Interface (port) for access token service"""

    def issue(self, payload: AccessTokenPayload, now: datetime) -> TokenVO: ...

    def verify(self, token: TokenVO) -> AccessTokenPayload: ...
