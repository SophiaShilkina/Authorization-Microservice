from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterUserResult:
    id: UUID
    email: str


@dataclass(frozen=True, slots=True)
class LoginUserResult:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class RefreshTokenResult:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LogoutAllUserResult:
    revoked_sessions: int
