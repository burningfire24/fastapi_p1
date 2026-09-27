from sqlalchemy.ext.asyncio import AsyncSession
from typing import List,Annotated

from sqlalchemy import select, or_


from src.db.schema import Base, User

#Create
async def create_user(name:str,email:str,phone:str,password:str,book_list:List[str],session:AsyncSession)->str:

    # Execute a single query checking for either email or phone
    stmt = select(User).where(or_(User.email == email, User.phone == phone))
    result = await session.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user==None:
        user = User(name=name, email=email,phone=phone,password=password,book_list=book_list)
        session.add(user)
        await session.commit()
        await session.refresh(user)  # loads generated id, etc.
        return "ok"
    else:
        return "not ok"


#Read
#from sqlalchemy import select, or_

async def get_users_by_email(email:str,session:AsyncSession):

    query=select(Users).where(User.email==email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_users_by_phone(phone:str,session:AsyncSession):

    query=select(Users).where(User.phone==phone)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def get_users_booklist(email:str,session:AsyncSession):
    query = select(User.book_list).where(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


#update
from sqlalchemy import update, func    
from sqlalchemy.ext.asyncio import AsyncSession

async def update_book_list(email:str,book:str, session:AsyncSession):

    query = (
        update(User)
        .where(User.email == email)
        .values(book_list=func.json_insert(User.book_list, book))
    )
    await session.execute(query)
    await session.commit()    
    
    book_lists = await get_users_booklist(email,session)

    return book_list




#Delete

from sqlalchemy import inspect

async def remove_user(email:str,session:AsyncSession):
    
    # 1. Fetch the user first
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # 2. Delete if user exists
    if user:
        await session.delete(user)
        await session.commit()

    # Check ORM state inspector
    state = inspect(user)
    if state.was_deleted:
        return f"User {user_id} was successfully removed."


