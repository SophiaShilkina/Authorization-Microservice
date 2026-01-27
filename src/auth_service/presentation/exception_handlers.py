from fastapi import FastAPI

from . import exceptions
from auth_service.domain.exceptions import (
    ValidationError as DomainValidationError,
    Violation as DomainViolation
)
from auth_service.application.exceptions import (
    ValidationError as AppValidationError,
    Violation as AppViolation,
    AuthError
)
from auth_service.infrastructure.expections import SecurityError


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DomainValidationError, exceptions.domain_validation_handler)
    app.add_exception_handler(DomainViolation, exceptions.domain_violation_handler)

    app.add_exception_handler(AppValidationError, exceptions.app_validation_handler)
    app.add_exception_handler(AppViolation, exceptions.app_violation_handler)
    app.add_exception_handler(AuthError, exceptions.app_auth_error_handler)

    app.add_exception_handler(SecurityError, exceptions.infra_security_handler)
