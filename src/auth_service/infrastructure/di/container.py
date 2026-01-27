from dishka import make_container, Container

from .providers import InfrastructureProvider, PolicyProvider, UseCaseProvider
from ..config import Config


def create_container() -> Container:
    config = Config.load()

    return make_container(
        InfrastructureProvider(),
        PolicyProvider(),
        UseCaseProvider(),
        context={Config: config},
    )
