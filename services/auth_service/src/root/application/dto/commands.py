from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    email: str
    username: str
    password: str
    context: ContextDTO


@dataclass(frozen=True, slots=True)
class LoginUserCommand:
    email: str
    password: str
    context: ContextDTO


@dataclass(frozen=True, slots=True)
class RefreshTokenCommand:
    refresh_token: str
    access_token: str


@dataclass(frozen=True, slots=True)
class LogoutUserCommand:
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LogoutAllUserCommand:
    access_token: str


@dataclass(frozen=True, slots=True)
class ContextDTO:
    ip: str
    user_agent: str
