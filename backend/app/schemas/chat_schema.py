from typing import List
from pydantic import BaseModel, Field

from model.chat_model import ChatModel


class ChatGetResponse(ChatModel):
    pass


class ChatListResponse(BaseModel):
    chats: List[ChatModel] = Field(..., description="Chats")


class ChatGenerateRequest(BaseModel):
    user_query: str = Field(..., description="User query")


class ChatGenerateResponse(ChatModel):
    pass
