from pydantic_settings import BaseSettings
from pydantic import Field

from . import schemas


class Config(BaseSettings):
    app: schemas.AppConfig = Field(default_factory=schemas.AppConfig)

    postgres: schemas.PostgresConfig = Field(default_factory=schemas.PostgresConfig)
    redis: schemas.RedisConfig = Field(default_factory=schemas.RedisConfig)
    kafka: schemas.KafkaConfig = Field(default_factory=schemas.KafkaConfig)

    fastapi: schemas.FastAPIConfig = Field(default_factory=schemas.FastAPIConfig)
    cors: schemas.CORSConfig = Field(default_factory=schemas.CORSConfig)
    cookie: schemas.CookieConfig = Field(default_factory=schemas.CookieConfig)

    access_token: schemas.AccessTokenConfig = Field(default_factory=schemas.AccessTokenConfig)
    refresh_token: schemas.RefreshTokenConfig = Field(default_factory=schemas.RefreshTokenConfig)

    rate_limit: schemas.RateLimitConfig = Field(default_factory=schemas.RateLimitConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
