import logging
import os
import uuid
from typing import Iterable, List, Optional, Tuple

from pinecone import PineconeAsyncio, ServerlessSpec
from pinecone_text.sparse import BM25Encoder

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

            # 3072 is the default dimension for the text-embedding-3-large model
            await db_instance.create_index(
                name=name,
                dimension=dimension or 3072,
                metric="dotproduct",
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

        sparse_embeddings = BM25Encoder.default().encode_documents(texts)

        for i, text in enumerate(texts):
            embedding = await self.create_openai_embedding(text)
            metadata = metadatas[i] if metadatas else {}
            metadata[self._text_key] = text

            sparse_embedding = sparse_embeddings[i]

            docs.append(
                {
                    "id": ids[i],
                    "values": embedding,
                    "sparse_values": {
                        "indices": sparse_embedding["indices"],
                        "values": sparse_embedding["values"],
                    },
                    "metadata": metadata,
                }
            )

        # upsert to Pinecone
        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            pc_index = pc.IndexAsyncio(host["host"])

            await pc_index.upsert(vectors=docs, namespace=partition)

        return ids

    async def search(  # pylint: disable=too-many-locals
        self,
        query: str,
        search_filter: Optional[dict] = None,
        partitions: Optional[List[str]] = None,
    ) -> List[Tuple[str, str, float]]:
        """
        Return pinecone documents most similar to query, along with scores.

        Output: (Retrieved text, metadata, score)
        """
        query_obj = await self.create_openai_embedding(query)
        query_obj_sparse = BM25Encoder.default().encode_queries(query)

        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            index = pc.IndexAsyncio(host["host"])

            results = await index.query_namespaces(
                vector=query_obj,
                sparse_vector=query_obj_sparse,
                metric="dotproduct",
                namespaces=partitions,
                top_k=20,  # maybe a bit too much but idk
                include_metadata=True,
                include_values=False,
                show_progress=False,
                filter=search_filter,
                alpha=0.75,
            )

            documents = []
            for result in results["matches"]:
                metadata = result["metadata"]
                if self._text_key in metadata:
                    text = metadata.pop(self._text_key)
                    documents.append(
                        {self._text_key: text, "id": result["id"], "metadata": metadata}
                    )

            reranked_results = await pc.inference.rerank(
                model="bge-reranker-v2-m3",
                query=query,
                documents=documents,
                top_n=10,
                return_documents=True,
                rank_fields=[self._text_key],
            )

            docs = []
            for res in reranked_results.data:
                metadata = res.document["metadata"]
                text = res.document[self._text_key]
                score = res.score
                docs.append((text, metadata, score))

            return docs

    async def remove_by_partition(self, partition: str):
        async with self.db_instance as pc:
            host = await pc.describe_index(self.index_name)
            pc_index = pc.IndexAsyncio(host["host"])
            await pc_index.delete(delete_all=True, namespace=partition)
