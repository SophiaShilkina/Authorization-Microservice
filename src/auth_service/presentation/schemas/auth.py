from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description='Почта пользователя',
        examples=['user@example.com']
    )
    password: SecretStr = Field(
        ...,
        description="Пароль пользователя"
    )


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
