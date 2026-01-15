class DomainValidationError(Exception):
    pass


class EmailAlreadyExistsExc(DomainValidationError):
    pass


class AuthorizationFailed(DomainValidationError):
    pass


class AuthenticationFailed(DomainValidationError):
    pass
