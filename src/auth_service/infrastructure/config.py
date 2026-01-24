from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
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


class RedisConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='redis_')

    # Redis Data Source Name
    host: str
    port: int

    # Client settings
    encoding = 'utf-8'
    decode_responses = True

    @property
    def dsn(self) -> str:
        """Возвращает DSN для redis"""
        return f'redis://{self.host}:{self.port}'


class FastAPIConfig(ConfigBase):
    host: str = 'localhost'
    port: int = 8000


class AccessTokenConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='access_token_')

    secret_key: SecretStr
    algorithm: str
    ttl_minutes: int = 15


class RefreshTokenConfig(ConfigBase):
    ttl_days: int = 7


class CookieConfig(ConfigBase):
    name: str = 'refresh_token'
    httponly: bool = True
    secure: bool = False
    samesite: str = "lax"
    max_age: int = 30 * 24 * 60 * 60


# ========== Config ==============

class Config(BaseSettings):
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)

    access_token: AccessTokenConfig = Field(default_factory=AccessTokenConfig)
    refresh_token: RefreshTokenConfig = Field(default_factory=RefreshTokenConfig)
    cookie: CookieConfig = Field(default_factory=CookieConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
