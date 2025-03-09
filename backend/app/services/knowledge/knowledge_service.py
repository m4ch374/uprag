import logging
from fastapi import HTTPException, UploadFile, status

from app.database.repository.user_repository import UserRepository
from services.knowledge.utils import KnowledgeUtils
from vector_db.pinecone import PineconeDB
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
    logger = logging.getLogger(__name__)

    @classmethod
    async def process_file(
        cls, token_data: TokenData, file: UploadFile
    ) -> KnowledgeUploadResponse:
        try:
            db = MongoDB.get_database()
            document_repo = DocumentRepository(db)

            parser = await UnstructuredDocumentParser.parse(file)

            if not parser.is_valid_file_type():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=KnowledgeErrorMessages.INVALID_FILE_TYPE,
                )

            document = await document_repo.add(
                {
                    "name": parser.file_name,
                    "created_by": token_data.user_id,
                    "file_size": parser.file_size,
                    "file_mime_type": parser.file_type,
                    "file_extension": parser.file_extension,
                }
            )

            res = await parser.generate_chunks()

            texts = [elem.get("text") for elem in res.elements if elem.get("text")]
            for i, text in enumerate(texts):
                if i:
                    cls.logger.info("=========================\n")
                cls.logger.info(text)

            metadatas = [{"content": text} for text in texts]

            collection_name = KnowledgeUtils.get_rag_index_name(token_data.user_id)
            await PineconeDB.create_collection(collection_name)
            pc = PineconeDB(index=collection_name)
            await pc.add_entry(texts, partition=document.id, metadatas=metadatas)

            return KnowledgeUploadResponse(**document.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error adding document to Pinecone: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def get_knowledges(cls, token_data: TokenData) -> KnowledgeListResponse:
        try:
            db = MongoDB.get_database()
            document_repo = DocumentRepository(db)

            documents = await document_repo.list_all({"created_by": token_data.user_id})

            return KnowledgeListResponse(
                knowledges=[
                    KnowledgeGetResponse(**doc.model_dump(by_alias=True))
                    for doc in documents
                ]
            )
        except Exception as e:
            cls.logger.error("Error getting knowledges: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def get_knowledge(
        cls, token_data: TokenData, knowledge_id: str
    ) -> KnowledgeGetResponse:
        try:
            db = MongoDB.get_database()
            document_repo = DocumentRepository(db)
            document = await document_repo.get(knowledge_id)
            if not document or document.created_by != token_data.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            return KnowledgeGetResponse(**document.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error getting knowledge with id %s: %s", knowledge_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def delete_knowledge(cls, token_data: TokenData, knowledge_id: str) -> None:
        try:
            db = MongoDB.get_database()
            document_repo = DocumentRepository(db)
            document = await document_repo.get(knowledge_id)
            if not document or document.created_by != token_data.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            user_repo = UserRepository(db)
            user = await user_repo.get(token_data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            await user_repo.update(
                user.id,
                {"knowledge": [k for k in user.knowledge if k != knowledge_id]},
                {},
            )
            await document_repo.delete(knowledge_id)

            pc = PineconeDB(index=KnowledgeUtils.get_rag_index_name(token_data.user_id))
            await pc.remove_by_partition(knowledge_id)

            return SuccessOperation(success=True)
        except Exception as e:
            cls.logger.error("Error deleting knowledge with id %s: %s", knowledge_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
