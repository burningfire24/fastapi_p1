from fastapi import APIRouter, Depends, Body, Header
from pydantic import EmailStr
from typing import Union, Annotated
from sqlalchemy.ext.asyncio import AsyncSession


from src.security.schema import Token
from src.security.hashing import get_password_hash,verify_password
from src.security.token_jwt import create_access_token, get_current_user
from .schema import user_schema,LogiIn,TokenChecker
from .services import create_user,get_users_booklist
from src.db.database import db_connection
from src.db.services import UserService


user_router = APIRouter()
user_service = UserService()

@user_router.post('/sing-up',response_model=Union[Token, str])
async def new_user(user_data:user_schema,db:AsyncSession=Depends(db_connection)):
    
    user_data.password = get_password_hash(user_data.password)

    db_res= await user_service.create_user(user_data,db)

    print(db_res)

    try:
        if db_res!="not ok":
            #create jwt
            token = await create_access_token({"name":user_data.name,"email":user_data.email})
            return Token(access_token=token, token_type="bearer")

        return "user already exists"    

    except Exception as e:
        print(f"===============error is {e}===================================")  



@user_router.get('/login')
async def existing_user(cred:Annotated[LogiIn,Header()],session:AsyncSession=Depends(db_connection)):

    get_db_data = await user_service.get_users_by_email(cred.email,session)
    
    if get_db_data:
        if verify_password(cred.password,get_db_data.password):
            #provide jwt
            token = await create_access_token({"name":get_db_data.name, "email":get_db_data.email})
            return Token(access_token=token,token_type="bearer")

        else:
           return  {
                "msg":"incorrect password"
            }

    else :        
        return {
            "msg":"invalid credentials"
        }

    


@user_router.get('/get_data')
async def get_users_booklist(
    token:Annotated[TokenChecker,Header()],
    db:AsyncSession=Depends(db_connection)
):

    
    token_value = token.model_dump()
    #validate token
    is_token_valid= await get_current_user(token_value)
    #get data from db
    if is_token_valid:
        email=is_token_valid['email']
        data= await get_users_booklist(email)
        return data
    else:
        return "invalid users"
  




@user_router.patch('/update')
async def update_user(db:AsyncSession=Depends(db_connection)):
    
    #validate token

    #update data into db
    
    #response to user
    pass

@user_router.delete('/remove')
async def remove_user(db:AsyncSession=Depends(db_connection)):

    #validate token

    #get data from db
    
    #response to user

    pass






    