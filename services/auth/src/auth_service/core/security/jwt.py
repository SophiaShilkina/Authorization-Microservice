from datetime import datetime, timedelta
from typing import Dict, Any
from uuid import uuid4

from jose import jwt, JWTError

from auth_service import config


class JWTService:
    def __init__(self):
        self._secret_key = config.jwt.secret_key
        self._algorithm = config.jwt.algorithm
        self._access_token_expire_minutes = config.jwt.access_token_expire_minutes

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Создание JWT access токена"""
        to_encode = data.copy()

        to_encode.update({
            "iat": int(datetime.now().timestamp()),
            "exp": int((datetime.now() + timedelta(minutes=self._access_token_expire_minutes)).timestamp()),
            "jti": uuid4().hex,
        })

        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Декодирование JWT access токена"""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError:
            return {}


jwt_service = JWTService()
