from pydantic_settings import BaseSettings
from pydantic import Field

from . import env


class Config(BaseSettings):
    postgres: env.PostgresConfig = Field(default_factory=env.PostgresConfig)
    auth: env.AuthConfig = Field(default_factory=env.AuthConfig)
    fastapi: env.FastAPIConfig = Field(default_factory=env.FastAPIConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
