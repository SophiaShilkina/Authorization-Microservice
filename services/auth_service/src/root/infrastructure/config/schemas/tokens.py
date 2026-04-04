from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr

from .base import ConfigBase


class AccessTokenConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='access_token_')

    public_key: SecretStr
    private_key: SecretStr
    algorithm: str
    ttl_minutes: int = 15


class RefreshTokenConfig(ConfigBase):
    ttl_days: int = 7
