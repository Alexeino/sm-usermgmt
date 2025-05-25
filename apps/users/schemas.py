from pydantic import BaseModel, Field, EmailStr
from datetime import date
from enum import Enum as PyEnum

class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    
class UserRole(PyEnum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    STAFF = "staff"
    ADMIN = "admin"
    
class UserBase(BaseModel):
    first_name: str
    email: EmailStr
    role: UserRole

    middle_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    phone_no: str | None = None
    

class UserCreate(UserBase):
    password: str = Field(min_length=8)