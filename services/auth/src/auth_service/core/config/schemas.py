from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr

BASE_DIR = Path(__file__).resolve().parents[4]
SETTINGS_PATH = BASE_DIR / 'settings'


# =========== Base schema ==============

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=(SETTINGS_PATH / '.env.template', SETTINGS_PATH / '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )


# =========== Main schemas =============

class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    # Postgres Data Source Name
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    # Engine settings
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 20
    max_overflow: int = 10

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
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class FastAPIConfig(ConfigBase):
    host: str = 'localhost'
    port: int = 8000
