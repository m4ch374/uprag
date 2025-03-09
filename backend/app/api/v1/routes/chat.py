import logging
from fastapi import APIRouter, Body, Depends, HTTPException, status

from utils.error_messages import GeneralErrorMessages
from schemas.chat_schema import (
    ChatContinueRequest,
    ChatContinueResponse,
    ChatGenerateRequest,
    ChatGenerateResponse,
    ChatGetResponse,
    ChatListResponse,
)
from schemas.auth_schema import TokenData
from services.chat.chat_service import ChatService
from services.auth.utils import AuthUtils


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ChatListResponse,
    response_model_by_alias=False,
)
async def get_chats(
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> ChatListResponse:
    try:
        logger.info("Getting chats")
        data = await ChatService.get_chats(token_data)
    except HTTPException as e:
        logger.error("Error getting chats: %s", e)
        raise e
    except Exception as e:
        logger.error("Error getting chats: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data


@router.get(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChatGetResponse,
    response_model_by_alias=False,
)
async def get_chat(
    chat_id: str,
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> ChatGetResponse:
    try:
        logger.info("Getting chat with id %s", chat_id)
        data = await ChatService.get_chat(chat_id, token_data)
    except HTTPException as e:
        logger.error("Error getting chat with id %s: %s", chat_id, e)
        raise e
    except Exception as e:
        logger.error("Error getting chat with id %s: %s", chat_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ChatGenerateResponse,
    response_model_by_alias=False,
)
async def start_chat(
    token_data: TokenData = Depends(AuthUtils.verify_token),
    body: ChatGenerateRequest = Body(...),
) -> ChatGenerateResponse:
    try:
        logger.info("Generating chat")
        data = await ChatService.start_chat(token_data, body)
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


@router.post(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChatContinueResponse,
    response_model_by_alias=False,
)
async def continue_chat(
    chat_id: str,
    token_data: TokenData = Depends(AuthUtils.verify_token),
    body: ChatContinueRequest = Body(...),
) -> ChatContinueResponse:
    try:
        logger.info("Continuing chat with id %s", chat_id)
        data = await ChatService.continue_chat(chat_id, token_data, body)
    except HTTPException as e:
        logger.error("Error continuing chat with id %s: %s", chat_id, e)
        raise e
    except Exception as e:
        logger.error("Error continuing chat with id %s: %s", chat_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data
