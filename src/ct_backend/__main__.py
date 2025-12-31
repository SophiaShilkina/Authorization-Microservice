from app import app
from utils import setup_logging
from ct_backend import config
import uvicorn


if __name__ == "__main__":
    setup_logging()

    uvicorn.run(
        app,
        host=config.fastapi.host,
        port=config.fastapi.port
    )
