from fastapi import FastAPI

from . import handlers
from root.domain.exceptions import (
    ValidationError as DomainValidationError,
    Violation as DomainViolation
)
from root.application.exceptions import (
    ValidationError as AppValidationError,
    Violation as AppViolation,
    AuthError
)
from root.infrastructure.exceptions import SecurityError


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DomainValidationError, handlers.domain_validation_handler)
    app.add_exception_handler(DomainViolation, handlers.domain_violation_handler)

    app.add_exception_handler(AppValidationError, handlers.app_validation_handler)
    app.add_exception_handler(AppViolation, handlers.app_violation_handler)
    app.add_exception_handler(AuthError, handlers.app_auth_error_handler)

    app.add_exception_handler(SecurityError, handlers.infra_security_handler)
