import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from utils.error_messages import GeneralErrorMessages
from services.knowledge.knowledge_service import KnowledgeService
from services.auth.utils import AuthUtils
from schemas.auth_schema import TokenData
from schemas.knowledge_schema import KnowledgeUploadResponse


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=KnowledgeUploadResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def upload_file(
    file: UploadFile = File(...),
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> KnowledgeUploadResponse:
    """
    Allows the user to upload a file as knowledge to a workspace.
    """
    try:
        logger.info("Uploading file %s", file.filename)
        data = await KnowledgeService.process_file(token_data, file)
    except HTTPException as e:
        logger.error("Error uploading file: %s", e)
        raise e
    except Exception as e:
        logger.error("Error uploading file: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data
