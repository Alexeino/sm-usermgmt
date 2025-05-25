from db.base import Base
from db.mixins import TimeStampModelMixin
from sqlalchemy import Column, String, Date, Enum as SQLEnum, select
from apps.users.schemas import UserCreate, Gender, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from apps.base.utils import Hasher
from pydantic import EmailStr
from fastapi import HTTPException, status
from typing import Any
class User(TimeStampModelMixin, Base):
    first_name = Column(String,nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String,nullable=True)
    date_of_birth = Column(Date,nullable=True)
    gender = Column(SQLEnum(Gender,name="gender"))
    
    
    email = Column(String,nullable=False,unique=True)
    phone_no = Column(String,nullable=True)
    
    password_hash = Column(String,nullable=False)
    
    role = Column(SQLEnum(UserRole,name="user_role"),nullable=False)

    @classmethod
    async def create(cls,user_data: UserCreate, db:AsyncSession):
        if await cls.get_user(email=user_data.email,db=db):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_data.email} already exists!"
            )
        user_data_dict = cls.update_hash_password(user_data)
        user = User(**user_data_dict)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @classmethod
    async def get_user(cls,email: EmailStr, db: AsyncSession):
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    def update_hash_password(cls,user_data: UserCreate) -> Any:
        password_hash = Hasher.get_pwd_hash(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["password_hash"] = password_hash
        user_data_dict.pop("password")
        return user_data