from pydantic import BaseModel, EmailStr
from typing import List

class user_schema(BaseModel):
    name:str
    email:EmailStr
    phone:str
    password:str
    book_list:List[str]


class LogiIn(BaseModel):
    email:str
    password:str



class TokenChecker(BaseModel):
    access_token:str
    token_type:str
