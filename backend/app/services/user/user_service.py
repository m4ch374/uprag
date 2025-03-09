import logging

from fastapi import HTTPException, status
from schemas.auth_schema import TokenData
from schemas.user_schema import UserPatchRequest, UserPatchResponse
from utils.error_messages import GeneralErrorMessages
from database.repository.user_repository import UserRepository
from database.database import MongoDB


class UserService:
    logger = logging.getLogger(__name__)

    @classmethod
    async def update_user(
        cls, token_data: TokenData, update_query: UserPatchRequest
    ) -> UserPatchResponse:
        try:
            db = MongoDB.get_database()
            user_repo = UserRepository(db)

            user = await user_repo.get(token_data.user_id)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            res = await user_repo.update(
                user.id,
                update_query.model_dump(by_alias=True, exclude_unset=True),
                {},
            )

            return UserPatchResponse(**res.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error updating user: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
