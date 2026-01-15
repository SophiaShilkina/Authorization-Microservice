from typing import Protocol

from auth_service.domain.value_objects import PasswordVO, AccessTokenVO
from ..dto import AccessTokenPayloadDTO


class IPasswordHasher(Protocol):
    """Interface (port) for password hashing service"""

    def get_password_hash(self, password: PasswordVO) -> str: ...

    def verify(self, plain_password: PasswordVO, hashed_password: str) -> bool: ...

    def dummy_verify(self, plain_password: PasswordVO) -> None: ...


class ITokenService(Protocol):
    """Interface (port) for token service"""

    def issue_refresh_token(self) -> tuple[str, str]:
        """:returns: raw_token, hashed_token"""

    def hash_token(self, raw_token: str) -> str: ...

    def issue_access_token(self, payload: AccessTokenPayloadDTO) -> AccessTokenVO: ...

    def verify_access_token(self, token: str) -> AccessTokenPayloadDTO: ...
