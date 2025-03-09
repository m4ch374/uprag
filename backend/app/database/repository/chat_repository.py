from model.chat_model import ChatModel
from database.repository.repository import Repository


class ChatRepository(Repository[ChatModel]):
    def __init__(self, db):
        super().__init__(db, "chat", ChatModel)
