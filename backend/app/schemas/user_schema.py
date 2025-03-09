from typing import List
from pydantic import BaseModel, Field

from model.user_model import UserModel


class UserPatchRequest(BaseModel):
    knowledge: List[str] = Field(..., description="List of document id")


class UserPatchResponse(UserModel):
    pass
