from .base import ConfigBase


class FastAPIConfig(ConfigBase):
    host: str = 'localhost'
    port: int = 8000


class CookieConfig(ConfigBase):
    name: str = 'refresh_token'
    httponly: bool = True
    secure: bool = True
    samesite: str = 'lax'
    max_age: int = 30 * 24 * 60 * 60
