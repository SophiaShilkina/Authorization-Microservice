import secrets

import hashlib

from auth_service import config


class RandomTokenService:
    def __init__(self):
        self.refresh_token_expire_days = config.random_token.refresh_token_expire_days

    @staticmethod
    def create_refresh_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
