from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr

from config import SETTINGS_PATH


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SETTINGS_PATH / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="postgres_")

    host: str
    password: SecretStr
