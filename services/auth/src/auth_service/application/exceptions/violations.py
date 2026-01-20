from .base import ApplicationError


class BusinessRuleViolation(ApplicationError):
    pass


class AlreadyExists(BusinessRuleViolation):
    pass


class RateLimitExceeded(BusinessRuleViolation):
    pass
