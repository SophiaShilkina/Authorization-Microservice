from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RegisterUserResult:
    id: UUID
    email: str
    username: str


@dataclass(frozen=True, slots=True)
class LoginUserResult:
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class RefreshTokenResult:
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class LogoutAllUserResult:
    revoked_sessions: int
