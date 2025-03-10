# pylint: disable=attribute-defined-outside-init
from io import BytesIO
import os
from pathlib import Path
from typing import List, Optional

from fastapi import UploadFile
import unstructured_client
from unstructured_client.models import shared
from utils.document_parser.document_parser import (
    DEFAULT_ACCEPTED_FILE_TYPES,
    DocumentParser,
)


# pylint: disable=too-many-instance-attributes
class UnstructuredDocumentParser(DocumentParser):
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
        return await self.client.general.partition_async(
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
