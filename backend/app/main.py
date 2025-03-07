import os
import logging

from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from database.database import MongoDB

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(server_app: FastAPI):
    try:
        logger.info("starting server")
        logger.info(server_app)  # to keep pylint happy
        MongoDB.initialize(os.environ["MONGODB_URL"], os.environ["MONGODB_DB_NAME"])
        yield
        logger.info("stopping server")
    except Exception as e:
        logger.error("uh oh, lifespan issue %s", e)


app = FastAPI(title="uprag", lifespan=lifespan)


@app.get("/")
def read_root():
    logger.info("read root")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
