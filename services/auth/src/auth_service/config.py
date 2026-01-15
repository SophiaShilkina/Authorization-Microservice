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


class FastAPIConfig(ConfigBase):
    host: str = 'localhost'
    port: int = 8000


class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='jwt_')

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int = 30


class RandomTokenConfig(ConfigBase):
    refresh_token_expire_days: int = 7


class CookieConfig(ConfigBase):
    name: str = "refresh_token"
    httponly: bool = True
    # TODO: secure = True в проде
    secure: bool = False
    samesite: str = "lax"
    max_age: int = 30 * 24 * 60 * 60


# ========== Config ==============

class Config(BaseSettings):
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    random_token: RandomTokenConfig = Field(default_factory=RandomTokenConfig)
    cookie: CookieConfig = Field(default_factory=CookieConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()  # type: ignore
