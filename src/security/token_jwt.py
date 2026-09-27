import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from .schema import Token

from .config import config

from datetime import datetime, timedelta, timezone

#not sure code
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import asyncio

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


async def get_current_user(token: Annotated[Token, Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

   
    try:
        payload = jwt.decode(token["access_token"], config.secret_key, algorithms=[config.algorithm])
        return payload

    except InvalidTokenError:
        raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )        








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