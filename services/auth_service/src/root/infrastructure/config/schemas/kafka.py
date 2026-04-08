from pydantic_settings import SettingsConfigDict

from .base import ConfigBase


class RedpandaConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='kafka_')

    # Kafka Data Source Name
    host: str
    kafka_api_port: int
    shema_registry_port: int
    kafka_http_proxy_port: int

    @property
    def kafka_api_dsn(self) -> str:
        """Возвращает DSN для Kafka API"""
        return (
            f'http://{self.host}:{self.kafka_api_port}'
        )
    @property
    def shema_registry_dsn(self) -> str:
        """Возвращает DSN для Schema Registry"""
        return (
            f'http://{self.host}:{self.shema_registry_port}'
        )

    @property
    def kafka_http_proxy_dsn(self) -> str:
        """Возвращает DSN для Kafka HTTP Proxy"""
        return (
            f'http://{self.host}:{self.kafka_http_proxy_port}'
        )

