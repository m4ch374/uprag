import logging
from fastapi import APIRouter, Depends, status

from schemas.auth_schema import TokenData
from services.auth.utils import AuthUtils


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/onboard", status_code=status.HTTP_201_CREATED)
async def onboard(token_data: TokenData = Depends(AuthUtils.verify_token)):
    logging.info(token_data)
    return {"message": "onboard"}
