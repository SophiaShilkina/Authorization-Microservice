from pydantic_settings import BaseSettings, TomlConfigSettingsSource
from pydantic import Field

from config import SETTINGS_PATH
from .models import env, toml


class Config(BaseSettings):
    postgres: env.PostgresConfig = Field(default_factory=env.PostgresConfig)
    fastapi: toml.FastapiConfig

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        toml_path = SETTINGS_PATH / "config.toml"
        return (TomlConfigSettingsSource(settings_cls, toml_path),)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
