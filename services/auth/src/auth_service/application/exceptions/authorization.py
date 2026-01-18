from .base import ApplicationError


class AuthError(ApplicationError):
    pass


class AuthenticationFailed(AuthError):
    pass


class TokenExpired(AuthenticationFailed):
    pass


class AuthorizationError(AuthError):
    pass


class PermissionDenied(AuthorizationError):
    pass
