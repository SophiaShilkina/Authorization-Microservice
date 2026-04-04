from pydantic_settings import SettingsConfigDict

from .base import ConfigBase


class KafkaConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='kafka_')

    # Kafka Data Source Name
    host: str
    port: int

    @property
    def dsn(self) -> str:
        """Возвращает DSN для kafka"""
        return (
            f'http://{self.host}:{self.port}'
        )

