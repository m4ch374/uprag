from typing import List
from pydantic import BaseModel, Field
from model.common_model import MongoDBObject


class KnowledgeGetResponse(MongoDBObject):
    name: str = Field(..., description="File name")
    created_by: str = Field(..., description="User who uploaded the file")
    file_mime_type: str = Field(..., description="File MIME type")
    file_extension: str = Field(..., description="File extension")
    file_size: int = Field(..., description="File size")


class KnowledgeListResponse(BaseModel):
    knowledges: List[KnowledgeGetResponse] = Field(
        ..., description="List of knowledge files"
    )


class KnowledgeUploadResponse(BaseModel):
    name: str = Field(..., description="File name")
    file_mime_type: str = Field(..., description="File MIME type")
    file_extension: str = Field(..., description="File extension")
    created_by: str = Field(..., description="User who uploaded the file")
    file_size: int = Field(..., description="File size")
