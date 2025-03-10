# pylint: disable=attribute-defined-outside-init
from io import BytesIO
import logging
import os
from pathlib import Path
from typing import List, Optional

from fastapi import UploadFile
import unstructured_client
from unstructured_client.models import shared
from utils.agent.chatgpt_agent import ChatGPTAgent
from utils.document_parser.document_parser import (
    DEFAULT_ACCEPTED_FILE_TYPES,
    DocumentParser,
)
from utils.prompt_templates.contextual_chunking import CONTEXTUAL_CHUNK_TEMPLATE


# pylint: disable=too-many-instance-attributes
class UnstructuredDocumentParser(DocumentParser):
    logger = logging.getLogger(__name__)
    unstructured_api_key: str = os.environ["UNSTRUCTURED_API_KEY"]
    unstructured_server_url: str = "https://api.unstructured.io/general/v0/general"

    client = unstructured_client.UnstructuredClient(
        api_key_auth=unstructured_api_key,
        server_url=unstructured_server_url,
    )

    chunk_overlap: int = 36
    chunk_size: int = 512

    @staticmethod
    async def parse(
        file: UploadFile,
        accepted_file_types: Optional[List[str]] = None,
        chunk_overlap: int = chunk_overlap,
        chunk_size: int = chunk_size,
    ):
        parser = UnstructuredDocumentParser()
        parser.file = file
        parser.file_name = file.filename
        parser.file_type = file.content_type
        parser.file_extension = Path(file.filename).suffix

        parser.file_size = len(await file.read())
        await file.seek(0)

        parser.parser_accepted_file_types = (
            accepted_file_types or DEFAULT_ACCEPTED_FILE_TYPES
        )

        parser.chunk_overlap = chunk_overlap
        parser.chunk_size = chunk_size

        return parser

    async def generate_chunks(self):
        await self.file.seek(0)
        return dict(
            await self.client.general.partition_async(
                request={
                    "partition_parameters": {
                        "files": {
                            "content": BytesIO(await self.file.read()).read(),
                            "file_name": self.file_name,
                            "content_type": self.file_type,
                        },
                        "strategy": shared.Strategy.HI_RES,
                        "chunking_strategy": "by_title",  # why did enum for chunk strategy disappear :(
                        "overlap": self.chunk_overlap,
                        "max_characters": self.chunk_size,
                    }
                }
            )
        )

    # an implementation of Anthropic's Contextual Chunking
    async def generate_contextual_chunks(self):
        chunks = await self.generate_chunks()
        await self.file.seek(0)  # reset just in case

        chunk_texts = [
            elem.get("text") for elem in chunks["elements"] if elem.get("text")
        ]
        whole_document = "\n".join(chunk_texts)

        for i, chunk in enumerate(chunk_texts):
            gpt_agent = ChatGPTAgent(
                model="gpt-4o",
                system_prompt=CONTEXTUAL_CHUNK_TEMPLATE(whole_document, chunk),
            )

            contextualized_chunk = await gpt_agent.generate_response(chunk)

            chunks["elements"][i]["text"] = (
                contextualized_chunk.choices[0].message.content
                + chunks["elements"][i]["text"]
            )

        return chunks
