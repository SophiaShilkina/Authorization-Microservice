from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr


class RegisterResponse(BaseModel):
    id: UUID
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str


class RefreshResponse(BaseModel):
    access_token: str


class LogoutResponse(BaseModel):
    pass


class LogoutAllResponse(BaseModel):
    revoked_sessions: int
