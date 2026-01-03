import uvicorn

from app import app
from auth_service.utils import setup_logging
from auth_service import config


if __name__ == "__main__":
    setup_logging()

    # TODO: убрать reload в проде
    uvicorn.run(
        "main:app",
        host=config.fastapi.host,
        port=config.fastapi.port,
        reload=True,
    )
