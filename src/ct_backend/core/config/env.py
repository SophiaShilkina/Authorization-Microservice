from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SETTINGS_PATH = PROJECT_ROOT / 'settings'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SETTINGS_PATH / '.env', env_file_encoding='utf-8', extra='ignore'
    )


class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def dsn(self) -> str:
        """Возвращает DSN для asyncpg"""
        return (
            f'postgresql+asyncpg://{self.user}:'
            f'{self.password.get_secret_value()}@'
            f'{self.host}:{self.port}/{self.db}'
        )


class AuthConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='auth_')

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class FastAPIConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='fastapi_')

    host: str
    port: int
