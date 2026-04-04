from fastapi import Request

from .base import error_response
from root.infrastructure.exceptions import SecurityError, InvalidAccessToken


def infra_security_handler(_: Request, exc: SecurityError):
    status = 404
    if isinstance(exc, InvalidAccessToken):
        status = 401

    return error_response(
        status_code=status,
        error_type=SecurityError,
        exc=exc,
    )
