from utils.prompt_templates.rag_template import RAG_TEMPLATE
from utils.agent.chatgpt_agent import ChatGPTAgent
from schemas.auth_schema import TokenData
from schemas.chat_schema import ChatGenerateResponse


class ChatService:
    @staticmethod
    async def complete_chat(
        token_data: TokenData, message: str
    ) -> ChatGenerateResponse:
        gpt_agent = ChatGPTAgent(
            model="gpt-4o",
            system_prompt=RAG_TEMPLATE,
            temperature=0.6,
            user_id=token_data.user_id,
        )

        response = await gpt_agent.generate_response(message, rag=True)

        return ChatGenerateResponse(
            assistant_response=response.choices[0].message.content
        )
