from .base import InfrastructureError


class PersistenceError(InfrastructureError):
    pass


class NotFoundError(PersistenceError):
    pass
