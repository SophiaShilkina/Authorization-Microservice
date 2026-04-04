from .base import ConfigBase


class FastAPIConfig(ConfigBase):
    host: str = 'localhost'
    port: int = 8000


class CORSConfig(ConfigBase):
    # Prod
    origins: list = [
        'http://localhost',
    ]
    credentials: bool = True
    methods: list = ['POST', 'OPTIONS']
    headers: list = ['Content-Type', 'Authorization']

    # Dev
    # origins: list = [
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    #     "http://localhost:5173",
    #     "http://127.0.0.1:5173",
    # ]
    # credentials: bool = True
    # methods: list = ['*']
    # headers: list = ['*']


class CookieConfig(ConfigBase):
    name: str = 'refresh_token'
    httponly: bool = True
    secure: bool = True
    samesite: str = 'lax'
    max_age: int = 30 * 24 * 60 * 60
