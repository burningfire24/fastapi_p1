from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import jwt



from src.security.schema import Token
from src.security.hashing import get_password_hash, verify_password
from src.security.token_jwt import create_access_token, get_current_user,refresh_token_request
from .schema import user_schema, LogiIn,RefreshTokenRequest
from src.db.database import db_connection
from src.db.services import UserService

user_router = APIRouter()
user_service = UserService()



@user_router.post('/sing-up')
async def new_user(user_data: user_schema, db: AsyncSession = Depends(db_connection)):
    user_data.password = get_password_hash(user_data.password)
    db_res = await user_service.create_user(user_data, db)
    print(f"data as per below {db_res}")
    if db_res:
        # Create access token (30 minutes default)
        access_token = create_access_token({
            "name": user_data.name,
            "email": user_data.email
        })
        
        # Create refresh token (7 days default)
        refresh_token = create_access_token(
            {"name": user_data.name, "email": user_data.email},
            is_refresh=True
        )
        
        return JSONResponse({
            "msg": "User created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": user_data.email
        })
    
    return JSONResponse({"msg": "User already exists"}, status_code=400)

@user_router.post('/login')
async def existing_user(cred: LogiIn, session: AsyncSession = Depends(db_connection)):
    get_db_data = await user_service.get_users_by_email(cred.email, session)
    
    if get_db_data and verify_password(cred.password, get_db_data.password):
        # Create access token
        access_token = create_access_token({
            "name": get_db_data.name,
            "email": get_db_data.email
        })
        
        # Create refresh token
        refresh_token = create_access_token(
            {"name": get_db_data.name, "email": get_db_data.email},
            is_refresh=True
        )
        
        return JSONResponse({
            "msg": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": get_db_data.email
        })
    
    return JSONResponse({"msg": "Invalid credentials"}, status_code=401)

@user_router.post('/refresh')
async def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:

        payload = await refresh_token_request(refresh_request)
        # Create new access token
        new_access_token = create_access_token({
            "name": payload.get("name"),
            "email": payload.get("email")
        })
        
        return JSONResponse({
            "msg": "Token refreshed successfully",
            "access_token": new_access_token,
            "token_type": "bearer"
        })
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

@user_router.get('/get_data')
async def get_users_booklist(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(db_connection)
):
    # current_user contains the decoded token payload
    email = current_user.get("email")
    
    # Get user data from database
    user_data = await user_service.get_users_by_email(email, db)
    
    if user_data:
        return {
            "name": user_data.name,
            "email": user_data.email,
            "book_list": user_data.book_list
        }
    
    return JSONResponse({"msg": "User data not found"}, status_code=404)
  




@user_router.patch('/update')
async def update_user( 
    add_book_to_list:str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(db_connection)
):
    # Update user logic here
    email = current_user.get('email')
    try:
        user_update= await user_service.update_book_list(email,add_book_to_list,db)
        if user_update:
            return user_update

        return {"msg": "something went wrong"}
    except Exception as e:
        print(f"failed with error {e}")
        raise e    



@user_router.delete('/remove')
async def remove_user(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(db_connection)
):
    # Delete user logic here
    return {"msg": "Delete endpoint - implement user deletion logic"}






    