import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timedelta, timezone

from .config import config
from src.usersely.schema import RefreshTokenRequest
# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None, is_refresh: bool = False) -> str:
    """Create JWT token (access or refresh)"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default: 30 minutes for access token, 7 days for refresh token
        if is_refresh:
            expire = datetime.now(timezone.utc) + timedelta(days=config.refresh_token_expire_days)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=config.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "refresh" if is_refresh else "access"})
    encoded_jwt = jwt.encode(to_encode, config.secret_key.get_secret_value(), algorithm=config.algorithm)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Dependency to get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            config.secret_key.get_secret_value(), 
            algorithms=[config.algorithm]
        )
        
        # Check if it's a refresh token trying to access protected route
        if payload.get("type") == "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token cannot be used for access"
            )
            
        return payload
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired"
        )
    except InvalidTokenError:
        raise credentials_exception

async def refresh_token_request(refresh_request: RefreshTokenRequest):

    payload = jwt.decode(
        refresh_request.refresh_token,
        config.secret_key.get_secret_value(),
        algorithms=[config.algorithm]
    )
    

    # Verify it's actually a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    return payload





# payload  = asyncio.run(create_access_token({
#     "name":"kabutar",
#     "job":"unemployed"
# }))  

# print(payload)

# payload = {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoia2FidXRhciIsImpvYiI6InVuZW1wbG95ZWQiLCJleHAiOjE3OTAyNTQxODZ9.rZtld8X3jEXDrH-oLvS6KOVxoAst5x8iovjnFQ4QoTM",
#   "token_type": "bearer"
# }

# verify = asyncio.run(get_current_user(payload))

# print(verify)