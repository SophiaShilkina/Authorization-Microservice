from .base import ApplicationError


class ValidationError(ApplicationError):
    pass


class InvalidTypeError(ValidationError):
    pass


class InvalidLengthError(ValidationError):
    pass


class InvalidFormatError(ValidationError):
    pass


class EmptyValueError(ValidationError):
    pass
