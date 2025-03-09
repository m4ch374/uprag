import asyncio
import logging
from fastapi import HTTPException, status
from services.chat.chat_utils import ChatUtils
from database.repository.document_repository import DocumentRepository
from database.database import MongoDB
from database.repository.chat_repository import ChatRepository
from utils.error_messages import GeneralErrorMessages
from utils.prompt_templates.rag_template import RAG_TEMPLATE
from utils.agent.chatgpt_agent import ChatGPTAgent
from schemas.auth_schema import TokenData
from schemas.chat_schema import (
    ChatContinueRequest,
    ChatContinueResponse,
    ChatGenerateRequest,
    ChatGenerateResponse,
    ChatGetResponse,
    ChatListResponse,
    ChatModifyRequest,
    ChatModifyResponse,
)


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
        cls, token_data: TokenData, body: ChatGenerateRequest
    ) -> ChatGenerateResponse:
        try:
            db = MongoDB.get_database()

            if body.knowledge:
                document_repo = DocumentRepository(db)
                documents = await document_repo.list_all(
                    {"_id": {"$in": body.knowledge}}
                )

                all_owned = all(d.created_by == token_data.user_id for d in documents)

                if not all_owned:
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
                body.user_query, rag=len(body.knowledge), partitions=body.knowledge
            )

            chat = await chat_repo.add(
                {
                    "created_by": token_data.user_id,
                    "chat_title": body.user_query,
                    "history": ChatUtils.history_to_string(gpt_agent.history),
                    "knowledge": body.knowledge,
                }
            )

            return ChatGenerateResponse(**chat.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error generating chat: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def continue_chat(
        cls, chat_id: str, token_data: TokenData, body: ChatContinueRequest
    ) -> ChatGenerateResponse:
        try:
            db = MongoDB.get_database()

            if body.knowledge:
                document_repo = DocumentRepository(db)
                documents = await document_repo.list_all(
                    {"_id": {"$in": body.knowledge}}
                )

                all_owned = all(d.created_by == token_data.user_id for d in documents)

                if not all_owned:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=GeneralErrorMessages.NOT_FOUND,
                    )

            chat_repo = ChatRepository(db)
            chat = await chat_repo.get(chat_id)
            if not chat or chat.created_by != token_data.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            if body.knowledge != chat.knowledge:
                asyncio.create_task(
                    chat_repo.update(chat_id, {"knowledge": body.knowledge}, {})
                )

            gpt_agent = ChatGPTAgent(
                model="gpt-4o",
                system_prompt=RAG_TEMPLATE,
                temperature=0.6,  # less variation is g
                user_id=token_data.user_id,
                initial_history=ChatUtils.string_to_history(chat.history),
            )
            await gpt_agent.generate_response(
                body.user_query, rag=len(body.knowledge), partitions=body.knowledge
            )

            chat = await chat_repo.update(
                chat_id,
                {"history": ChatUtils.history_to_string(gpt_agent.history)},
                {},
            )

            return ChatContinueResponse(**chat.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error continuing chat with id %s: %s", chat_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    async def modify_chat(
        cls, chat_id: str, body: ChatModifyRequest, token_data: TokenData
    ) -> ChatModifyResponse:
        try:
            db = MongoDB.get_database()

            chat_repo = ChatRepository(db)
            chat = await chat_repo.get(chat_id)
            if not chat or chat.created_by != token_data.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=GeneralErrorMessages.NOT_FOUND,
                )

            if body.knowledge:
                document_repo = DocumentRepository(db)
                documents = await document_repo.list_all(
                    {"_id": {"$in": body.knowledge}}
                )

                all_owned = all(d.created_by == token_data.user_id for d in documents)

                if not all_owned:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=GeneralErrorMessages.NOT_FOUND,
                    )

            new_chat = await chat_repo.update(chat_id, body, {})

            return ChatModifyResponse(**new_chat.model_dump(by_alias=True))
        except Exception as e:
            cls.logger.error("Error modifying chat with id %s: %s", chat_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
