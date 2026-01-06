from pydantic_settings import BaseSettings
from pydantic import Field

from . import schemas


class Config(BaseSettings):
    postgres: schemas.PostgresConfig = Field(default_factory=schemas.PostgresConfig)
    fastapi: schemas.FastAPIConfig = Field(default_factory=schemas.FastAPIConfig)
    jwt: schemas.JWTConfig = Field(default_factory=schemas.JWTConfig)
    random_token: schemas.RandomTokenConfig = Field(default_factory=schemas.RandomTokenConfig)
    cookie: schemas.CookieConfig = Field(default_factory=schemas.CookieConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
