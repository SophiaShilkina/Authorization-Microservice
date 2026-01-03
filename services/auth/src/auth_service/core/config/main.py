from pydantic_settings import BaseSettings
from pydantic import Field

from . import schemas


class Config(BaseSettings):
    postgres: schemas.PostgresConfig = Field(default_factory=schemas.PostgresConfig)
    auth: schemas.AuthConfig = Field(default_factory=schemas.AuthConfig)
    fastapi: schemas.FastAPIConfig = Field(default_factory=schemas.FastAPIConfig)
    api_prefix: schemas.APIPrefixConfig = Field(default_factory=schemas.APIPrefixConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
