import uvicorn

from application import app
from auth_service.utils import setup_logging
from auth_service import config


if __name__ == "__main__":
    setup_logging()

    # TODO: убрать reload в проде
    uvicorn.run(
        app,
        host=config.fastapi.host,
        port=config.fastapi.port
    )
