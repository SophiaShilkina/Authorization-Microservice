from pydantic_settings import SettingsConfigDict
from pydantic.types import SecretStr

from .base import ConfigBase


class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    # Postgres Data Source Name
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    # Engine secrets
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

    # Client secrets
    encoding: str = 'utf-8'
    decode_responses: bool = True

    @property
    def dsn(self) -> str:
        """Возвращает DSN для redis"""
        return f'redis://{self.host}:{self.port}'
