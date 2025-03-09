import logging
import os
import uuid
from typing import Iterable, List, Optional, Tuple

from pinecone import PineconeAsyncio, ServerlessSpec

from vector_db.vector_db import VectorDB

logger = logging.getLogger(__name__)


class PineconeDB(VectorDB):
    def __init__(self, index) -> None:
        super().__init__()
        self.pinecone_api_key = os.environ["PINECONE_API_KEY"]

        self.index_name = index
        self.db_instance = PineconeAsyncio(api_key=self.pinecone_api_key)
        self._text_key = "content"

    @staticmethod
    async def create_collection(name, dimension: Optional[int] = None):
        async with PineconeAsyncio(
            api_key=os.environ["PINECONE_API_KEY"]
        ) as db_instance:
            if await db_instance.has_index(name):
                return

            # 1536 is the default dimension for the text-embedding-3-small model
            await db_instance.create_index(
                name=name,
                dimension=dimension or 1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

    async def add_entry(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        partition: Optional[str] = "",
    ) -> List[str]:
        # Embed and create the documents
        docs = []
        ids = ids or [str(uuid.uuid4()) for _ in texts]

        for i, text in enumerate(texts):
            embedding = await self.create_openai_embedding(text)
            metadata = metadatas[i] if metadatas else {}
            metadata[self._text_key] = text
            docs.append({"id": ids[i], "values": embedding, "metadata": metadata})

        # upsert to Pinecone
        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            pc_index = pc.IndexAsyncio(host["host"])

            await pc_index.upsert(vectors=docs, namespace=partition)

        return ids

    async def search(
        self,
        query: str,
        search_filter: Optional[dict] = None,
        partitions: Optional[List[str]] = None,
    ) -> List[Tuple[str, str, float]]:
        """
        Return pinecone documents most similar to query, along with scores.
        """
        query_obj = await self.create_openai_embedding(query)
        docs = []

        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            index = pc.IndexAsyncio(host["host"])

            results = await index.query_namespaces(
                vector=query_obj,
                metric="cosine",
                namespaces=partitions or self.config.partitions,
                top_k=self.config.top_k,
                include_metadata=True,
                include_values=False,
                show_progress=False,
                filter=search_filter,
            )

        for res in results["matches"]:
            metadata = res["metadata"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                score = res["score"]
                docs.append((text, metadata, score))
            else:
                logger.warning(
                    "Found document with no `%s` key. Skipping.", self._text_key
                )

        return docs

    async def remove_by_partition(self, partition: str):
        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            pc_index = pc.IndexAsyncio(host["host"])
            await pc_index.delete(delete_all=True, namespace=partition)
