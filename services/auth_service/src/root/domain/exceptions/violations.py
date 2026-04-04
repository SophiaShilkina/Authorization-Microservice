from .base import DomainError


class Violation(DomainError):
    pass


class InvariantViolation(Violation):
    pass


class BusinessRuleViolation(Violation):
    pass
