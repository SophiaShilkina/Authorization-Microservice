from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr


class RegisterResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str


class RefreshRequest(BaseModel):
    refresh_token: SecretStr


class RefreshResponse(BaseModel):
    access_token: str


class LogoutRequest(BaseModel):
    refresh_token: SecretStr


class LogoutResponse(BaseModel):
    pass


class LogoutAllResponse(BaseModel):
    revoked_sessions: int
