import logging
from fastapi import APIRouter, Depends, HTTPException, status

from utils.error_messages import GeneralErrorMessages
from schemas.auth_schema import AuthOnboardResponse, TokenData
from services.auth.auth_service import AuthService
from services.auth.utils import AuthUtils


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/onboard", status_code=status.HTTP_201_CREATED)
async def onboard(
    token_data: TokenData = Depends(AuthUtils.verify_token),
) -> AuthOnboardResponse:
    try:
        data = await AuthService.onboard_user(token_data)
    except HTTPException as e:
        logger.error("Error onboarding user: %s", e)
        raise e
    except Exception as e:
        logger.error("Error onboarding user: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
        ) from e

    logger.info("/auth/onboard endpoint invocation success")
    return data
