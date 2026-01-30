from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: str


class RefreshRequest(BaseModel):
    refresh_token: SecretStr


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: str


class LogoutRequest(BaseModel):
    refresh_token: SecretStr


class LogoutResponse(BaseModel):
    pass


class LogoutAllRequest(BaseModel):
    access_token: str
    access_token_expires_at: datetime


class LogoutAllResponse(BaseModel):
    revoked_sessions: int
