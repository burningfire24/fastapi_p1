from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from .config import config


class Token(BaseModel):
    access_token:str
    token_type:str



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    
    return encoded_jwt

