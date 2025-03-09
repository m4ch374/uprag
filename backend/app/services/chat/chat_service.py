from fastapi import HTTPException, status
from database.database import MongoDB
from database.repository.user_repository import UserRepository
from utils.error_messages import GeneralErrorMessages
from utils.prompt_templates.rag_template import RAG_TEMPLATE
from utils.agent.chatgpt_agent import ChatGPTAgent
from schemas.auth_schema import TokenData
from schemas.chat_schema import ChatGenerateResponse


class ChatService:
    @staticmethod
    async def complete_chat(
        token_data: TokenData, message: str
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

            gpt_agent = ChatGPTAgent(
                model="gpt-4o",
                system_prompt=RAG_TEMPLATE,
                temperature=0.6,
                user_id=token_data.user_id,
            )

            response = await gpt_agent.generate_response(
                message, rag=len(user.knowledge), partitions=user.knowledge
            )

            return ChatGenerateResponse(
                assistant_response=response.choices[0].message.content
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=GeneralErrorMessages.INTERNAL_SERVER_ERROR,
            ) from e
