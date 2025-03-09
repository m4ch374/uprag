from utils.agent.chatgpt_agent import ChatGPTAgent
from utils.prompt_templates.short_answer import SHORT_ANSWER_TEMPLATE
from schemas.auth_schema import TokenData
from schemas.chat_schema import ChatGenerateResponse


class ChatService:
    @staticmethod
    async def complete_chat(_: TokenData, message: str) -> ChatGenerateResponse:
        gpt_agent = ChatGPTAgent(
            model="gpt-4o",
            system_prompt=SHORT_ANSWER_TEMPLATE,
            temperature=0.6,
        )

        response = await gpt_agent.generate_response(message)

        return ChatGenerateResponse(
            assistant_response=response.choices[0].message.content
        )
