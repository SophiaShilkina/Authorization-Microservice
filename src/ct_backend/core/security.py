from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from ct_backend import config

pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__salt_len=16,
    argon2__hash_len=32,
)

class TokenService:
    def __init__(self):
        self.secret_key = config.auth.secret_key
        self.algorithm = config.auth.algorithm
        self.access_token_expire_minutes = config.auth.access_token_expire_minutes
        self.refresh_token_expire_days = config.auth.refresh_token_expire_days

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширование пароля"""
        return pwd_context.hash(password)

    def create_token(self, data: Dict[str, Any],
                     expires_delta: Optional[timedelta] = None,
                     token_type: str = "access") -> str:
        """Создание JWT токена"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            if token_type == "access":
                expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
            else:
                expire = datetime.now() + timedelta(days=self.refresh_token_expire_days)

        to_encode.update({
            "exp": expire,
            "type": token_type,
            "iat": datetime.now()
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Создание access токена"""
        return self.create_token(data, token_type="access")

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Создание refresh токена"""
        return self.create_token(data, token_type="refresh")

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Декодирование JWT токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return {}


token_service = TokenService()
