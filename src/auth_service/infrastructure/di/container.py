from dishka import make_container

from .providers import InfrastructureProvider, PolicyProvider, UseCaseProvider

container = make_container(
    InfrastructureProvider(),
    PolicyProvider(),
    UseCaseProvider(),
)
