from fastapi import APIRouter, Depends, HTTPException, status
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from apps.users.schemas import UserBase, UserCreate, UserRole
from apps.users.models import User
from pydantic import EmailStr

user_router = APIRouter(prefix="/users",tags=["Users App"])

@user_router.post("/create",response_model=UserBase)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await User.create(user_data,db)
    return user

@user_router.get("/get-customer",response_model=UserBase)
async def get_customer(email: EmailStr, db: AsyncSession = Depends(get_db)):
    customer = await User.get_user(email,UserRole.CUSTOMER,db)
    if customer:
        return customer
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User with Email: {email} not found!"
    )