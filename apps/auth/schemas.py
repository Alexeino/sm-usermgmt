from pydantic import BaseModel, Field, EmailStr

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    