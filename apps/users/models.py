from db.base import Base
from db.mixins import TimeStampModelMixin
from sqlalchemy import Column, String, Date, Enum as SQLEnum, select
from apps.users.schemas import UserCreate, Gender, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from apps.base.utils import Hasher
from pydantic import EmailStr

class User(TimeStampModelMixin, Base):
    first_name = Column(String,nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String,nullable=True)
    date_of_birth = Column(Date,nullable=True)
    gender = Column(SQLEnum(Gender,name="gender"))
    
    
    email = Column(String,nullable=False)
    phone_no = Column(String,nullable=True)
    
    password_hash = Column(String,nullable=False)
    
    role = Column(SQLEnum(UserRole,name="user_role"),nullable=False)

    @classmethod
    async def create(cls,user_data: UserCreate, db:AsyncSession):
        password_hash = Hasher.get_pwd_hash(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["password_hash"] = password_hash
        user_data_dict.pop("password")
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
