from typing import List, Optional
from pydantic import Field
from model.common_model import MongoDBObject


class ChatModel(MongoDBObject):
    created_by: str = Field(..., description="User who created the chat")
    chat_title: str = Field(..., description="Title of the chat")
    history: str = Field(..., description="String serialized chat history from json")
    knowledge: Optional[List[str]] = Field(
        default=[], description="Knowledge base used to generate the chat"
    )
