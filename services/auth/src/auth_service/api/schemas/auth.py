from typing import Optional, Literal
import re

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator


class UserCreateRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description='Почта, с которой регистрируется пользователь. Должна быть уникальной',
        examples=['user@example.com']
    )
    role: Literal['user', 'volunteer', 'shelter_worker'] = Field(
        ...,
        description='Роль пользователя',
        examples=['user', 'volunteer', 'shelter_worker']
    )
    password: SecretStr = Field(
        ...,
        min_length=8,
        description='Валидация: хотя бы одна строчная буква, хотя бы одна заглавная буква, хотя бы один специальный символ.',
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        """Валидация пароля: минимум 8 символов, заглавные и строчные буквы, специальные символы"""
        password = v.get_secret_value()

        if not re.search(r'[A-Z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')

        if not re.search(r'[a-z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')

        return v


class UserCreateResponse(BaseModel):
    id: int = Field(
        ...,
        description='ID пользователя в БД',
        examples=[1, 115, 123714]
    )
    email: EmailStr = Field(
        ...,
        description='Почта пользователя',
        examples=['user@example.com']
    )
    role: Literal['user', 'volunteer', 'shelter_worker'] = Field(
        ...,
        description='Роль пользователя',
        examples=['user', 'volunteer', 'shelter_worker']
    )


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
