import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status

from utils.error_messages import GeneralErrorMessages
from schemas.auth_schema import TokenData
from schemas.user_schema import UserGetResponse, UserPatchRequest, UserPatchResponse
from services.auth.utils import AuthUtils
from services.user.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserGetResponse,
    response_model_by_alias=False,
)
async def get_user(
    token_data: TokenData = Depends(AuthUtils.verify_token),
):
    try:
        logger.info("Getting user")
        data = await UserService.get_user(token_data)
    except HTTPException as e:
        logger.error("Error getting user: %s", e)
        raise e
    except Exception as e:
        logger.error("Error getting user: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data


@router.patch(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserPatchResponse,
    response_model_by_alias=False,
)
async def update_user(
    token_data: TokenData = Depends(AuthUtils.verify_token),
    body: UserPatchRequest = Body(...),
):
    try:
        logger.info("Updating user")
        data = await UserService.update_user(token_data, body)
    except HTTPException as e:
        logger.error("Error updating user: %s", e)
        raise e
    except Exception as e:
        logger.error("Error updating user: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    return data
