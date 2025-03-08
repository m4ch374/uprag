from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    user_id: str
    user_email: EmailStr
