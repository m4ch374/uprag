from io import BytesIO
import os
from pathlib import Path

import unstructured_client
from unstructured_client.models import shared
from fastapi import HTTPException, UploadFile, status

from utils.error_messages import KnowledgeErrorMessages
from services.knowledge.utils import KnowledgeUtils
from database.database import MongoDB
from database.repository.document_repository import DocumentRepository
from schemas.knowledge_schema import KnowledgeUploadResponse
from schemas.auth_schema import TokenData


class KnowledgeService:
    @classmethod
    async def process_file(  # pylint: disable=too-many-locals
        cls, token_data: TokenData, file: UploadFile
    ) -> KnowledgeUploadResponse:
        db = MongoDB.get_database()
        file_content = await file.read()

        document_repo = DocumentRepository(db)

        file_type = file.content_type
        if not KnowledgeUtils.is_valid_file_type(file_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=KnowledgeErrorMessages.INVALID_FILE_TYPE,
            )

        document = await document_repo.add(
            {
                "name": file.filename,
                "created_by": token_data.user_id,
                "file_size": len(file_content),
                "file_mime_type": file_type,
                "file_extension": Path(file.filename).suffix,
            }
        )

        client = unstructured_client.UnstructuredClient(
            api_key_auth=os.environ["UNSTRUCTURED_API_KEY"],
            server_url="https://api.unstructured.io/general/v0/general",
        )

        await file.seek(0)
        res = await client.general.partition_async(
            request={
                "partition_parameters": {
                    "files": {
                        "content": BytesIO(await file.read()).read(),
                        "file_name": file.filename,
                        "content_type": file_type,
                    },
                    "strategy": shared.Strategy.HI_RES,
                    "chunking_strategy": "by_title",
                    "overlap": 100,
                    "max_characters": 500,
                }
            }
        )

        texts = [elem.get("text") for elem in res.elements if elem.get("text")]
        for i, text in enumerate(texts):
            if i:
                print("=========================\n")
            print(text)

        # await PineconeDB.create_collection(f"rag-{workspace_id}")
        # pc = PineconeDB(PineconeConfig(index=f"rag-{workspace_id}"))
        # await pc.add_texts(texts, partition=document.id)

        return KnowledgeUploadResponse(**document.model_dump(by_alias=True))
