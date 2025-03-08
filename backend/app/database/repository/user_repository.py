from pymongo.database import Database

from database.repository.repository import Repository
from model.user_model import UserModel


class UserRepository(Repository[UserModel]):
    def __init__(self, db: Database):
        super().__init__(db, "users", UserModel)
