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
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def dsn(self) -> str:
        """Возвращает DSN для asyncpg"""
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/{self.db}"
        )
