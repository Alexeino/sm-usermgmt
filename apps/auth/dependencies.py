from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from apps.auth.utils import decode_token

class TokenBearer(HTTPBearer):
    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired Token !"
            )
            
        self.verify_token_data(token_data)
                
        return token_data
    
    def token_valid(self,token:str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True
        return False
    
    def verify_token_data(self,token_data: dict) -> None:
        raise NotImplementedError("Please override this method in child classes!")
    
class AccessTokenBearer(TokenBearer):
    
    def __init__(self,required_scope: str = None, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.required_scope = required_scope
    
    def verify_token_data(self,token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token!"
            )
        user_data = token_data.get("user",None)
        user_scopes = user_data.get("scopes",[])
        if "*" in user_scopes:
            return # Admin bypass
        
        if self.required_scope and self.required_scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough Permission. Require {self.required_scope} Scope"
            )

class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token!"
            )
            
access_token_bearer = AccessTokenBearer()