from .base import ApplicationError


class Violation(ApplicationError):
    pass


class BusinessRuleViolation(Violation):
    pass


class AlreadyExists(BusinessRuleViolation):
    pass


class UserAlreadyExists(AlreadyExists):
    pass


class RateLimitExceeded(BusinessRuleViolation):
    pass
