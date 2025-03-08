from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from utils.document_parser.unstructured_parser import UnstructuredDocumentParser
from utils.error_messages import KnowledgeErrorMessages
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
