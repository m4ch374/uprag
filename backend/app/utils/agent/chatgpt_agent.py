import os
from openai import AsyncOpenAI
from utils.agent.agent import Agent


class ChatGPTAgent(Agent):
    def __init__(self, model: str, system_prompt: str, temperature: float = 1):
        super().__init__(model, system_prompt, temperature)

        self.client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def __generate_initial_history__(self):
        return [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

    async def generate_chat_response(self, user_query: str):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                *self.history,
                {"role": "user", "content": user_query},
            ],
            temperature=self.temperature,
        )
        self.history.append({"role": "user", "content": user_query})
        self.history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return response
