import logging
from fastapi import HTTPException, status
from services.chat.chat_utils import ChatUtils
from database.database import MongoDB
from database.repository.chat_repository import ChatRepository
from database.repository.user_repository import UserRepository
from utils.error_messages import GeneralErrorMessages
from utils.prompt_templates.rag_template import RAG_TEMPLATE
from utils.agent.chatgpt_agent import ChatGPTAgent
from schemas.auth_schema import TokenData
from schemas.chat_schema import ChatGenerateResponse, ChatGetResponse, ChatListResponse


class ChatService:
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_chats(cls, token_data: TokenData) -> ChatListResponse:
        try:
            db = MongoDB.get_database()
            chat_repo = ChatRepository(db)
            chats = await chat_repo.list_all({"created_by": token_data.user_id})

            return ChatListResponse(
                chats=[
                    ChatGetResponse(**chat.model_dump(by_alias=True)) for chat in chats
                ]
            )
        except Exception as e:
            cls.logger.error("Error getting chats: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def get_chat(cls, chat_id: str, token_data: TokenData) -> ChatGetResponse:
        try:
            db = MongoDB.get_database()
            chat_repo = ChatRepository(db)
            chat = await chat_repo.get(chat_id)
            if not chat or chat.created_by != token_data.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            return ChatGetResponse(**chat.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error getting chat with id %s: %s", chat_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def start_chat(
        cls, token_data: TokenData, message: str
    ) -> ChatGenerateResponse:
        try:
            db = MongoDB.get_database()
            user_repo = UserRepository(db)

            user = await user_repo.get(token_data.user_id)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            chat_repo = ChatRepository(db)
            gpt_agent = ChatGPTAgent(
                model="gpt-4o",
                system_prompt=RAG_TEMPLATE,
                temperature=0.6,  # less variation is g
                user_id=token_data.user_id,
            )

            await gpt_agent.generate_response(
                message, rag=len(user.knowledge), partitions=user.knowledge
            )

            chat = await chat_repo.add(
                {
                    "created_by": token_data.user_id,
                    "chat_title": message,
                    "history": ChatUtils.history_to_string(gpt_agent.history),
                }
            )

            return ChatGenerateResponse(**chat.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error generating chat: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
