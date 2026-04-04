from fastapi import Request

from .base import error_response
from root.application.exceptions import (
    ValidationError as AppValidationError,
    Violation as AppViolation, RateLimitExceeded,
    AuthError, AuthenticationFailed, AuthorizationError,
)


def app_validation_handler(_: Request, exc: AppValidationError):
    return error_response(
        status_code=422,
        error_type=AppValidationError,
        exc=exc,
    )


def app_violation_handler(_: Request, exc: AppViolation):
    status = 429 if isinstance(exc, RateLimitExceeded) else 409

    return error_response(
        status_code=status,
        error_type=AppViolation,
        exc=exc,
    )


def app_auth_error_handler(_: Request, exc: AuthError):
    status = 404
    if isinstance(exc, AuthenticationFailed):
        status = 401
    elif isinstance(exc, AuthorizationError):
        status = 403

    return error_response(
        status_code=status,
        error_type=AuthError,
        exc=exc,
    )
