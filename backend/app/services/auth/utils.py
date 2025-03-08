import os
import logging
from typing import Annotated

import asyncio
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError
from pydantic import ValidationError

# pylint: disable=no-name-in-module
from utils.error_messages import AuthErrorMessages
from schemas.auth_schema import TokenData

token_auth_scheme = HTTPBearer()


class AuthUtils:
    logger = logging.getLogger(__name__)

    @classmethod
    async def verify_token(
        cls,
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(token_auth_scheme)
        ],
    ) -> TokenData:
        try:
            cls.logger.info("verifying token")
            decoded = await asyncio.to_thread(
                jwt.decode,
                credentials.credentials,
                os.environ["CLERK_JWKS_PUBLIC_KEY"],
                ["RS256"],
            )
            return TokenData(**decoded)

        except (ValidationError, PyJWTError) as e:
            cls.logger.error("Error invalid token: %s", e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthErrorMessages.INVALID_CREDENTIALS,
            ) from e

        except Exception as e:
            cls.logger.error("Error verifying clerk token: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=AuthErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
