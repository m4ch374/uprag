import logging

from fastapi import HTTPException, status

from utils.error_messages import AuthErrorMessages
from database.database import MongoDB
from database.repository.user_repository import UserRepository
from schemas.auth_schema import TokenData


class AuthService:
    logger = logging.getLogger(__name__)

    # its called onboard bc i cant think of a better name
    @classmethod
    async def onboard_user(cls, token_data: TokenData):
        """
        "Onboards" a user by creating a new entry in the database

        If user exists, do nothing and return 200

        Else, create and return 201
        """

        db = MongoDB.get_database()
        user_repo = UserRepository(db)

        user = await user_repo.get(token_data.user_id)

        if user:
            cls.logger.info("User already exists, returning 200")
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=AuthErrorMessages.USER_ALREADY_EXISTS,
            )

        await user_repo.add(
            {
                "user_email": token_data.user_email,
                "_id": token_data.user_id,
            }
        )

        cls.logger.info("Created user")
        return {"message": "onboard"}
