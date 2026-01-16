from .base import DomainError


class ValidationError(DomainError):
    pass


class InvalidTypeError(ValidationError):
    pass


class EmptyValueError(ValidationError):
    pass


class InvalidLengthError(ValidationError):
    pass


class InvalidFormatError(ValidationError):
    pass
