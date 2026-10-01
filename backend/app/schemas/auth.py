from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import ORMModel

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=3, max_length=80)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(ORMModel):
    id: int
    email: str
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
