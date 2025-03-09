from model.document_model import DocumentModel
from database.repository.repository import Repository


class DocumentRepository(Repository[DocumentModel]):
    def __init__(self, db):
        super().__init__(db, "documents", DocumentModel)
