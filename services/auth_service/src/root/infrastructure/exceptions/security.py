from .base import InfrastructureError


class SecurityError(InfrastructureError):
    pass


class InvalidAccessToken(SecurityError):
    pass
