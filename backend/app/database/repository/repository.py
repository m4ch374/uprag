import asyncio
from datetime import datetime, timezone
import logging
from typing import Generic, List, Optional, Type, TypeVar, Union

from model.common_model import MongoDBObject
from pymongo import ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.database import Database

T = TypeVar("T", bound=MongoDBObject)


class Repository(Generic[T]):
    def __init__(self, db: Database, collection_name: str, model: Type[T]):
        self.db: Database = db
        self.collection: Collection = getattr(self.db, collection_name)
        self.logger = logging.getLogger(__name__)
        self.model = model

    async def get(  # pylint: disable=W0102
        self,
        item_id: str,
        key: Optional[str] = "_id",
        session: Optional[ClientSession] = None,
        filters: Optional[dict] = {},
    ) -> Union[T, None]:
        entry = await self.collection.find_one(
            {key: item_id, **filters}, session=session
        )

        return await self.__mongo_to_pydantic__(entry)

    async def add(
        self,
        object_dict: dict,
    ) -> Union[T, None]:
        try:
            new_entry = self.model(**object_dict)
        except ValueError as e:
            self.logger.error("Error creating new entry: %s", e)
            raise e

        try:
            response = await self.collection.insert_one(
                new_entry.model_dump(by_alias=True)
            )

            response = await self.collection.find_one({"_id": response.inserted_id})

            return await self.__mongo_to_pydantic__(response)
        except Exception as e:
            self.logger.error("An error occurred: %s", e)
            raise e

    async def list_all(self, filters: dict) -> Optional[List[T]]:
        try:
            resp = self.collection.find(filters)
            elements = await resp.to_list(length=None)
            return [await self.__mongo_to_pydantic__(e) for e in elements]
        except Exception as e:
            self.logger.error("An error occured: %s", e)
            raise e

    async def update(  # pylint: disable=R0917
        self,
        item_id: str,
        update_fields: dict,
        filters: Optional[dict],
        key: Optional[str] = "_id",
    ) -> Union[bool, T]:
        try:
            valid_update_fields = {
                k: v for k, v in update_fields.items() if k in self.model.model_fields
            }
            valid_update_fields["updated_at"] = datetime.now(timezone.utc)

            response = await self.collection.find_one_and_update(
                {**{key: item_id}, **filters},
                {"$set": valid_update_fields},
                return_document=ReturnDocument.AFTER,
            )

            if not response:
                return False

            return await self.__mongo_to_pydantic__(response)
        except Exception as e:
            self.logger.error("An error occurred: %s", e)
            raise e

    async def delete(self, item_id: str) -> bool:
        try:
            await self.collection.delete_one({"_id": item_id})

            # lets assume its always successful, why not
            return True
        except Exception as e:
            self.logger.error("Error deleting item with id %s: %s", item_id, e)
            raise e

    async def __mongo_to_pydantic__(self, entry) -> Union[T, None]:
        if not entry:
            return None

        def conversion():
            return self.model(**entry)

        try:
            res = await asyncio.to_thread(conversion)
            return res
        except Exception as e:
            self.logger.error(
                "Error occured when converting from mongodb entry to pydantic object: %s\nEntry: %s",
                e,
                entry,
            )
            raise e
