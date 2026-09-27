from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func    
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from .schema import UserCreateModel,User

from sqlalchemy import select, or_


class UserService:


    #Read
    #from sqlalchemy import select, or_

    async def get_user_by_uuid(self, uui_id:str,session:AsyncSession):
        pass

    async def get_users_by_email(self,email:str,session:AsyncSession):

        query=select(User).where(User.email==email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    async def get_users_by_phone(self,phone:str,session:AsyncSession):

        query=select(User).where(User.phone==phone)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_users_booklist(self,email:str,session:AsyncSession):
        query = select(User.book_list).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    #Create
    #need to set the return type
    async def create_user(self,user_data:UserCreateModel,session:AsyncSession):

        data = user_data.model_dump()
        user = User(**data)

        existing_user = await self.get_users_by_email(user_data.email,session)

        if existing_user==None:
            session.add(user)
            await session.commit()
            await session.refresh(user)  # loads generated id, etc.
            return user  
        else:
            return "not ok"


    

    # #update
    # from sqlalchemy import update, func    
    # from sqlalchemy.ext.asyncio import AsyncSession

    async def update_book_list(self,email:str,book:str, session:AsyncSession):


        query = (
            update(User)
            .where(User.email == email)
            .values(book_list=func.json_insert(User.book_list, book))
        )
        await session.execute(query)
        await session.commit()    
        
        book_lists = await get_users_booklist(email,session)

        return book_list




    # #Delete

    # from sqlalchemy import inspect

    async def remove_user(self,email:str,session:AsyncSession):
        
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