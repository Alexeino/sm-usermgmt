from fastapi import APIRouter, Depends, HTTPException, status
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from apps.users.schemas import UserBase, UserCreate
from apps.users.models import User
from pydantic import EmailStr
from apps.auth.utils import create_access_token
from apps.auth.schemas import UserLoginModel
from datetime import timedelta, datetime
from settings.config import settings
from fastapi.responses import JSONResponse
from apps.base.utils import Hasher
from apps.auth.dependencies import access_token_bearer, RefreshTokenBearer

user_router = APIRouter(prefix="/users",tags=["Users App"])

@user_router.post("/create",response_model=UserBase)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await User.create(user_data,db)
    return user

@user_router.get("/get-customer",response_model=UserBase)
async def get_customer(email: EmailStr, db: AsyncSession = Depends(get_db),current_user = Depends(access_token_bearer)):
    customer = await User.get_user(email,db)
    if customer:
        return customer
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User with Email: {email} not found!"
    )
    
@user_router.post("/login")
async def login_users(login_data: UserLoginModel, db: AsyncSession = Depends(get_db)):
    email = login_data.email
    password = login_data.password
    
    user = await User.get_user(email,db)
    if user:
        password_valid = Hasher.verify_password(password,user.password_hash)
        
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': user.id
                },
                expiry = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY)
            )
            refresh_token = create_access_token(
                refresh = True,
                expiry = timedelta(days=settings.REFRESH_TOKEN_EXPIRY),
                user_data={
                    'email': user.email,
                    'user_id': user.id
                }
            )
            return JSONResponse(
                content={
                    "message":"Login succesful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "id":user.id
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password!"
    )
    
@user_router.get("/refresh_token")
async def get_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    print(expiry_timestamp)
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"],
            expiry = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY)
            
        )
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Expired Refresh Token"
    )