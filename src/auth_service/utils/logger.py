import logging
from pythonjsonlogger import json
import sys


def setup_logging():
    formatter = json.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s',
        rename_fields={
            'levelname': 'level',
            'asctime': 'timestamp',
            'name': 'logger'
        },
        static_fields={
            'service': 'CaringTails'
        }
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    fastapi_logger = logging.getLogger("uvicorn.access")
    fastapi_logger.handlers.clear()
    fastapi_logger.propagate = True

    logging.getLogger("uvicorn.error").propagate = False
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
