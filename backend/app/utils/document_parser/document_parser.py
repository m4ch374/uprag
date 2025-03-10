import logging
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile

DEFAULT_ACCEPTED_FILE_TYPES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # "application/pdf",
    # "text/plain",
    # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    # "text/xml",
]


class DocumentParser:
    file: UploadFile
    file_name: str
    file_size: int
    file_type: str
    file_extension: str
    parser_accepted_file_types: List[str] = DEFAULT_ACCEPTED_FILE_TYPES

    logger = logging.getLogger(__name__)

    @staticmethod
    async def parse(
        file: UploadFile,
        accepted_file_types: Optional[List[str]] = None,
    ):
        parser = DocumentParser()
        parser.file_name = file.filename
        parser.file_type = file.content_type
        parser.file_extension = Path(file.filename).suffix

        parser.file_size = len(await file.read())
        await file.seek(0)

        parser.parser_accepted_file_types = (
            accepted_file_types or DEFAULT_ACCEPTED_FILE_TYPES
        )

        return parser

    def is_valid_file_type(self):
        return self.file_type in self.parser_accepted_file_types

    async def generate_chunks(self):
        raise NotImplementedError("not implemented")

    async def generate_contextual_chunks(self):
        raise NotImplementedError("not implemented")
