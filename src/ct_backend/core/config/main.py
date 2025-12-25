from pydantic_settings import BaseSettings, TomlConfigSettingsSource
from pydantic import Field

from ct_backend import SETTINGS_PATH
from .models import toml
from .models import env


class Config(BaseSettings):
    postgres: env.PostgresConfig = Field(default_factory=env.PostgresConfig)
    auth: env.AuthConfig = Field(default_factory=env.AuthConfig)

    fastapi: toml.FastapiConfig

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        toml_path = SETTINGS_PATH / "config.toml"
        return (TomlConfigSettingsSource(settings_cls, toml_path),)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
