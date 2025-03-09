import os
from typing import List, Optional

from openai import AsyncOpenAI

from services.knowledge.utils import KnowledgeUtils
from vector_db.pinecone import PineconeDB
from utils.agent.agent import Agent
from utils.prompt_templates.vector_db_context_assistant_content import (
    CONTEXT_ASSISTANT_CONTENT,
)


class ChatGPTAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def __generate_initial_history__(self):
        return [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

    async def generate_chat_response(self, user_query: str):
        self.history.append({"role": "user", "content": user_query})
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=self.temperature,
        )
        self.history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return response

    async def generate_ragged_chat_response(
        self,
        user_query: str,
        user_id: Optional[str] = None,
        partitions: Optional[List[str]] = None,
    ):
        pinecone = PineconeDB(
            KnowledgeUtils.get_rag_index_name(user_id or self.user_id)
        )

        # partition is a placeholder
        # TODO: dynamic partitions
        search_result = await pinecone.search(
            user_query,
            partitions=partitions or [],
        )

        contents = [content for content, _, _ in search_result]
        self.history.append({"role": "user", "content": user_query})
        self.history.append(
            {"role": "assistant", "content": CONTEXT_ASSISTANT_CONTENT(contents)}
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=self.temperature,
        )
        self.history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return response
