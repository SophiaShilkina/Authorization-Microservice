from pydantic_settings import BaseSettings
from pydantic import Field

from . import schemas


class Config(BaseSettings):
    postgres: schemas.PostgresConfig = Field(default_factory=schemas.PostgresConfig)
    redis: schemas.RedisConfig = Field(default_factory=schemas.RedisConfig)

    fastapi: schemas.FastAPIConfig = Field(default_factory=schemas.FastAPIConfig)

    access_token: schemas.AccessTokenConfig = Field(default_factory=schemas.AccessTokenConfig)
    refresh_token: schemas.RefreshTokenConfig = Field(default_factory=schemas.RefreshTokenConfig)
    cookie: schemas.CookieConfig = Field(default_factory=schemas.CookieConfig)
    rate_limit: schemas.RateLimitConfig = Field(default_factory=schemas.RateLimitConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
