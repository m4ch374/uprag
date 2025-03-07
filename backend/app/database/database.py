import logging
from logging import Logger

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database


class MongoDB:
    client: MongoClient = None
    database: Database = None
    logger: Logger = logging.getLogger(__name__)

    @classmethod
    def initialize(cls, uri: str, db_name: str) -> None:
        cls.logger.info("Connecting to MongoDB...")
        cls.client = AsyncIOMotorClient(uri)
        cls.database = cls.client[db_name]

        try:
            cls.client.admin.command("ping")
        except Exception as e:
            cls.logger.error("fail to connect to MongoDB: %s", e)
            raise e

        cls.logger.info("MongoDB success or something")

    @classmethod
    def get_database(cls) -> Database:
        if cls.database is None:
            raise RuntimeError("Database is not initialized")

        return cls.database

    @classmethod
    def get_collection(cls, collection_name: str) -> Collection:
        if cls.database is None:
            raise RuntimeError(
                "Database is not initialized. Please call initialize() method first."
            )
        return cls.database[collection_name]
