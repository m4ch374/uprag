import logging
from fastapi import APIRouter, Body, Depends, HTTPException, status

from utils.error_messages import GeneralErrorMessages
from schemas.chat_schema import ChatGenerateRequest, ChatGenerateResponse
from schemas.auth_schema import TokenData
from services.chat.chat_service import ChatService
from services.auth.utils import AuthUtils


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ChatGenerateResponse,
    response_model_by_alias=False,
)
async def generate_chat(
    token_data: TokenData = Depends(AuthUtils.verify_token),
    body: ChatGenerateRequest = Body(...),
) -> ChatGenerateResponse:
    try:
        logger.info("Generating chat")
        data = await ChatService.complete_chat(token_data, body.user_query)
    except HTTPException as e:
        logger.error("Error generating chat: %s", e)
        raise e
    except Exception as e:
        logger.error("Error generating chat: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data
