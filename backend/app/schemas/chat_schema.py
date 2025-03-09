from pydantic import BaseModel, Field


class ChatGenerateRequest(BaseModel):
    user_query: str = Field(..., description="User query")


class ChatGenerateResponse(BaseModel):
    assistant_response: str = Field(..., description="Assistant response")
