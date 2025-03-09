from typing import Optional
from pydantic import Field

from model.common_model import MongoDBObject


class DocumentModel(MongoDBObject):
    name: str = Field(..., description="Document name")
    file_size: int = Field(..., description="File size")
    file_mime_type: str = Field(..., description="File MIME type")
    file_extension: Optional[str] = Field(..., description="File extension")
    created_by: str = Field(..., description="User who uploaded the document")
