from dishka import make_async_container, AsyncContainer

from .providers import (
    InfrastructureProvider,
    PolicyProvider,
    UseCaseProvider,
    PostgresProvider,
    KafkaProvider,
    ExecutorProvider
)
from ..config import Config


def create_container() -> AsyncContainer:
    config = Config.load()

    return make_async_container(
        InfrastructureProvider(),
        PolicyProvider(),
        UseCaseProvider(),
        PostgresProvider(),
        KafkaProvider(),
        ExecutorProvider(),
        context={Config: config},
    )
