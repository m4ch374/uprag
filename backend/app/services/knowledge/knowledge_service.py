from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from utils.document_parser.unstructured_parser import UnstructuredDocumentParser
from utils.error_messages import GeneralErrorMessages, KnowledgeErrorMessages
from database.database import MongoDB
from database.repository.document_repository import DocumentRepository
from schemas.common_schema import SuccessOperation
from schemas.knowledge_schema import (
    KnowledgeGetResponse,
    KnowledgeListResponse,
    KnowledgeUploadResponse,
)
from schemas.auth_schema import TokenData


class KnowledgeService:
    @classmethod
    async def process_file(  # pylint: disable=too-many-locals
        cls, token_data: TokenData, file: UploadFile
    ) -> KnowledgeUploadResponse:
        db = MongoDB.get_database()
        file_content = await file.read()

        document_repo = DocumentRepository(db)

        parser = await UnstructuredDocumentParser.parse(file)

        file_type = file.content_type
        if not parser.is_valid_file_type():
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

        res = await parser.generate_chunks()

        texts = [elem.get("text") for elem in res.elements if elem.get("text")]
        for i, text in enumerate(texts):
            if i:
                print("=========================\n")
            print(text)

        # await PineconeDB.create_collection(f"rag-{workspace_id}")
        # pc = PineconeDB(PineconeConfig(index=f"rag-{workspace_id}"))
        # await pc.add_texts(texts, partition=document.id)

        return KnowledgeUploadResponse(**document.model_dump(by_alias=True))

    @classmethod
    async def get_knowledges(cls, token_data: TokenData) -> KnowledgeListResponse:
        db = MongoDB.get_database()
        document_repo = DocumentRepository(db)

        documents = await document_repo.list_all({"created_by": token_data.user_id})

        return KnowledgeListResponse(
            knowledges=[
                KnowledgeGetResponse(**doc.model_dump(by_alias=True))
                for doc in documents
            ]
        )

    @classmethod
    async def get_knowledge(
        cls, token_data: TokenData, knowledge_id: str
    ) -> KnowledgeGetResponse:
        db = MongoDB.get_database()
        document_repo = DocumentRepository(db)
        document = await document_repo.get(knowledge_id)
        if not document or document.created_by != token_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=GeneralErrorMessages.NOT_FOUND,
            )

        return KnowledgeGetResponse(**document.model_dump(by_alias=True))

    @classmethod
    async def delete_knowledge(cls, token_data: TokenData, knowledge_id: str) -> None:
        db = MongoDB.get_database()
        document_repo = DocumentRepository(db)
        document = await document_repo.get(knowledge_id)
        if not document or document.created_by != token_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=GeneralErrorMessages.NOT_FOUND,
            )

        await document_repo.delete(knowledge_id)

        return SuccessOperation(success=True)
