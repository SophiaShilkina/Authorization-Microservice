from fastapi import Request

from .base import error_response
from root.domain.exceptions import (
    ValidationError as DomainValidationError,
    Violation as DomainViolation
)


def domain_validation_handler(_: Request, exc: DomainValidationError):
    return error_response(
        status_code=422,
        error_type=DomainValidationError,
        exc=exc,
    )


def domain_violation_handler(_: Request, exc: DomainViolation):
    return error_response(
        status_code=409,
        error_type=DomainViolation,
        exc=exc,
    )
