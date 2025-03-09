import os
from typing import Iterable, List, Optional, Tuple
from openai import AsyncOpenAI

DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


class VectorDB:
    @staticmethod
    async def create_collection(name, dimension):
        raise NotImplementedError("not implemented")

    async def create_openai_embedding(
        self, text, model=DEFAULT_OPENAI_EMBEDDING_MODEL
    ) -> List[float]:
        params = {
            "input": text,
            "model": model,
        }

        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        return list((await client.embeddings.create(**params)).data[0].embedding)

    async def add_entry(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        partition: Optional[str] = None,
    ) -> List[str]:
        raise NotImplementedError("not implemented")

    async def search(
        self,
        query: str,
        search_filter: Optional[dict] = None,
        partitions: Optional[List[str]] = None,
    ) -> List[Tuple[str, str, float]]:
        raise NotImplementedError("not implemented")
