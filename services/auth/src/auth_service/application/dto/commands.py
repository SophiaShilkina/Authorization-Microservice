from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    username: str
    password: str


@dataclass(frozen=True)
class RegisterUserResult:
    id: UUID
    email: str
    username: str


@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str
    context: dict


@dataclass(frozen=True)
class LoginUserResult:
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass(frozen=True)
class RefreshTokenCommand:
    refresh_token: str


@dataclass(frozen=True)
class RefreshTokenResult:
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass(frozen=True)
class LogoutUserCommand:
    refresh_token: str


@dataclass(frozen=True)
class LogoutAllUserCommand:
    access_token: str


@dataclass(frozen=True)
class LogoutAllUserResult:
    revoked_sessions: int
