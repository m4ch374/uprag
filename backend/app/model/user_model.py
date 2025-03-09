from typing import List, Optional
from pydantic import Field
from model.common_model import MongoDBObject


class UserModel(MongoDBObject):
    user_email: str = Field(..., description="email of the user")
    knowledge: Optional[List[str]] = Field(
        default=[], description="List of document id"
    )
