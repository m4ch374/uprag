import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from utils.error_messages import GeneralErrorMessages
from services.knowledge.knowledge_service import KnowledgeService
from services.auth.utils import AuthUtils
from schemas.common_schema import SuccessOperation
from schemas.auth_schema import TokenData
from schemas.knowledge_schema import (
    KnowledgeGetResponse,
    KnowledgeListResponse,
    KnowledgeUploadResponse,
)


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=KnowledgeListResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def get_knowledges(
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> KnowledgeListResponse:
    """
    Returns a list of all the knowledge files in the workspace.
    """
    try:
        logger.info("Getting knowledges")
        data = await KnowledgeService.get_knowledges(token_data)
    except HTTPException as e:
        logger.error("Error getting knowledges: %s", e)
        raise e
    except Exception as e:
        logger.error("Error getting knowledges: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data


@router.get(
    "/{knowledge_id}",
    response_model=KnowledgeGetResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def get_knowledge(
    knowledge_id: str,
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> KnowledgeGetResponse:
    """
    Returns a knowledge file by id.
    """
    try:
        logger.info("Getting knowledge with id %s", knowledge_id)
        data = await KnowledgeService.get_knowledge(token_data, knowledge_id)
    except HTTPException as e:
        logger.error("Error getting knowledge with id %s: %s", knowledge_id, e)
        raise e
    except Exception as e:
        logger.error("Error getting knowledge with id %s: %s", knowledge_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e
    return data


@router.delete(
    "/{knowledge_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_knowledge(
    knowledge_id: str,
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> SuccessOperation:
    """
    Deletes a knowledge file by id.
    """
    try:
        logger.info("Deleting knowledge with id %s", knowledge_id)
        data = await KnowledgeService.delete_knowledge(token_data, knowledge_id)
    except HTTPException as e:
        logger.error("Error deleting knowledge with id %s: %s", knowledge_id, e)
        raise e
    except Exception as e:
        logger.error("Error deleting knowledge with id %s: %s", knowledge_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e
    return data


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
