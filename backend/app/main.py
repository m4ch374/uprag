import os
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import MongoDB
from api.v1.api import api_router

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

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    logger.info("Hello world")
    return {"Hello": "World"}
