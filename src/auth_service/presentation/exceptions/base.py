import logging

from fastapi.responses import ORJSONResponse

logger = logging.getLogger(__name__)


def error_response(
    *,
    status_code: int,
    error_type: type,
    exc: Exception,
):
    logger.exception('Program error',
                     extra={
                         'error_type': error_type.__name__,
                         'error_code': exc.__class__.__name__,
                         'error_message': str(exc),
                     })

    return ORJSONResponse(
        status_code=status_code,
        content={
            'error': {
                'type': error_type.__name__,
                'code': exc.__class__.__name__,
                'message': str(exc),
            }
        },
    )
