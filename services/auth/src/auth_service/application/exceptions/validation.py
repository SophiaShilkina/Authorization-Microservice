from .base import ApplicationError


class ValidationError(ApplicationError):
    pass


class InvalidLengthError(ValidationError):
    pass


class InvalidFormatError(ValidationError):
    pass
