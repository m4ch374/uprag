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
from schemas.chat_schema import ChatGenerateResponse


class ChatService:
    logger = logging.getLogger(__name__)

    @classmethod
    async def complete_chat(
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
            chat = await chat_repo.get(token_data.user_id, key="created_by")
            chat_history = ChatUtils.string_to_history(chat.history) if chat else []

            gpt_agent = ChatGPTAgent(
                model="gpt-4o",
                system_prompt=RAG_TEMPLATE,
                temperature=0.6,  # less variation is g
                user_id=token_data.user_id,
                initial_history=chat_history,
            )

            await gpt_agent.generate_response(
                message, rag=len(user.knowledge), partitions=user.knowledge
            )

            if chat:
                chat = await chat_repo.update(
                    chat.id,
                    {"history": ChatUtils.history_to_string(gpt_agent.history)},
                    {},
                )
            else:
                chat = await chat_repo.add(
                    {
                        "created_by": token_data.user_id,
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
