from typing import Protocol
from datetime import timedelta

from auth_service.domain.value_objects import TokenVO, TokenHashVO, PasswordHashVO
from auth_service.application.security.policies import PasswordPolicy
from ..security.models import AccessToken, AccessTokenPayload


class IPasswordHasher(Protocol):
    """Interface (port) for password hashing service"""

    def get_password_hash(self, password: PasswordPolicy) -> PasswordHashVO: ...

    def verify(self, plain_password: PasswordPolicy, password_hash: PasswordHashVO) -> bool: ...

    def dummy_verify(self, plain_password: PasswordPolicy) -> None: ...


class ITokenService(Protocol):
    """Interface (port) for token service"""

    def issue_refresh_token(self) -> tuple[TokenVO, TokenHashVO]: ...

    def hash_token(self, raw_token: TokenVO) -> TokenHashVO: ...

    def issue_access_token(self, payload: AccessTokenPayload) -> AccessToken: ...

    def verify_access_token(self, token: AccessToken) -> AccessTokenPayload: ...


class IRateLimitStorage(Protocol):
    async def increment(self, key: str, window: timedelta) -> int: ...

    async def reset(self, key: str) -> None: ...
