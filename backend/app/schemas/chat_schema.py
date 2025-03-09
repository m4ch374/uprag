from typing import List
from pydantic import BaseModel, Field

from model.chat_model import ChatModel


class ChatGetResponse(ChatModel):
    pass


class ChatListResponse(BaseModel):
    chats: List[ChatModel] = Field(..., description="Chats")


class ChatGenerateRequest(BaseModel):
    user_query: str = Field(..., description="User query")
    knowledge: List[str] = Field(
        default=[], description="Knowledge base used to generate the chat"
    )


class ChatGenerateResponse(ChatModel):
    pass


class ChatContinueRequest(BaseModel):
    user_query: str = Field(..., description="User query")
    knowledge: List[str] = Field(
        default=[], description="Knowledge base used to generate the chat"
    )


class ChatContinueResponse(ChatModel):
    pass


class ChatModifyRequest(BaseModel):
    knowledge: List[str] = Field(
        default=[], description="Knowledge base used to generate the chat"
    )


class ChatModifyResponse(ChatModel):
    pass
