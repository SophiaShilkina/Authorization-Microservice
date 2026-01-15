from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RegisterCommand:
    email: str
    username: str
    password: str


@dataclass(frozen=True)
class RegisterResult:
    id: UUID
    email: str
    username: str


@dataclass(frozen=True)
class LoginCommand:
    email: str
    password: str
    context: dict


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str
