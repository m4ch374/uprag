from pydantic import BaseModel, EmailStr

from model.user_model import UserModel


class TokenData(BaseModel):
    user_id: str
    user_email: EmailStr


class AuthOnboardResponse(UserModel):
    pass
