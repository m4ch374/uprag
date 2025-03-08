from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class MongoDBObject(BaseModel):
    # optional bc sometimes we have id and sometimes we dont
    #
    # NOTE: turning to string bc pydantic is weird handling ObjectId
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")

    @field_serializer("id")
    def serialize_id(self, obj_id: str):
        return str(obj_id).strip()

    model_config = {
        "arbitrary_types_allowed": True,
    }
