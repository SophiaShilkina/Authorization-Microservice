class DomainValidationError(Exception):
    pass


class EmailAlreadyExistsExc(DomainValidationError):
    pass


class AuthorizationFailed(DomainValidationError):
    pass


class AuthenticationFailed(DomainValidationError):
    pass


class Unauthorized(DomainValidationError):
    pass


class TokenExpired(DomainValidationError):
    pass
