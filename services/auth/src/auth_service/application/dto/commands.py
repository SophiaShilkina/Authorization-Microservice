from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    email: str
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class LoginUserCommand:
    email: str
    password: str
    context: dict


@dataclass(frozen=True, slots=True)
class RefreshTokenCommand:
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LogoutUserCommand:
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LogoutAllUserCommand:
    access_token: str
    access_token_expires_at: datetime
