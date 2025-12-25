import logging
from functools import wraps
from typing import Callable, Optional

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def error_handler(error_message: str, is_specially_caused_error: bool, not_found_message: Optional[str] = None):
    """
    Декоратор для обработки ошибок в API endpoints
    :param error_message: Сообщение об ошибке для возврата клиенту
    :param is_specially_caused_error: Вызвана ли ошибка специально из кода или упала сама
    :param not_found_message: Сообщение для случая 404
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)

                if result is None and not_found_message:
                    return JSONResponse(
                        status_code=404,
                        content={
                            'status': 'Not Found',
                            'message': not_found_message
                        }
                    )

                return result

            except KeyError as error:
                logger.error('Endpoint error',
                             extra={
                                 'error': error,
                                 'is_specially_caused_error': is_specially_caused_error
                             })

                return JSONResponse(
                    status_code=400,
                    content={
                        'status': 'Bad Request',
                        'message': str(error_message),
                        'error': str(error),
                    }
                )

            except ValueError as error:
                logger.error('Endpoint error',
                             extra={
                                 'error': error,
                                 'is_specially_caused_error': is_specially_caused_error
                             })

                return JSONResponse(
                    status_code=404,
                    content={
                        'status': 'Not Found',
                        'message': str(error_message),
                        'error': str(error),
                    }
                )

            except AttributeError as error:
                logger.error('Endpoint error',
                             extra={
                                 'error': error,
                                 'is_specially_caused_error': is_specially_caused_error
                             })

                return JSONResponse(
                    status_code=409,
                    content={
                        'status': 'Conflict',
                        'message': str(error_message),
                        'error': str(error),
                    }
                )

            except TimeoutError as error:
                logger.error('Endpoint error',
                             extra={
                                 'error': error,
                                 'is_specially_caused_error': is_specially_caused_error
                             })

                return JSONResponse(
                    status_code=504,
                    content={
                        'status': 'Gateway Time Out',
                        'message': str(error_message),
                        'error': str(error),
                    }
                )

            except Exception as error:
                logger.error('Endpoint error',
                             extra={
                                 'error': error,
                                 'is_specially_caused_error': is_specially_caused_error
                             })

                return JSONResponse(
                    status_code=500,
                    content={
                        'status': 'Internal Server Error',
                        'message': f'{error_message}: {error}'
                    }
                )

        return wrapper

    return decorator
