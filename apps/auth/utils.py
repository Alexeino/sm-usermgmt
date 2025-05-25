from datetime import timedelta, datetime, timezone
import jwt
from settings.config import settings
import uuid
import logging

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now(timezone.utc) + expiry
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as  e:
        logging.exception(e)
        return None