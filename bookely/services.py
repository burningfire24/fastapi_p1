from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from .schema import CreateModel, Book

class BookService:

    async def get_book_by_uid(bookuid:str,session:AsyncSession):
        return await session.get(Book,bookuid)

    async def get_book_by_name(bookname:str,session:AsyncSession)->list[str]:
        #apply elasticSearch - return matching name with the kw searcg
        pass

    async def get_book_name_search(bookname:str,session:AsyncSession):
        #apply elasticSearch - return matching name with the kw searcg
        try:
            query = select(Book).where(Book.Title == bookname)
            result = await session.execute(query)
            return result.scalars().first()
        except Exception as e:
            print(f"Error:{e}")
            raise HTTPException(status_code=500,detail=str("something went wrong"))    
        

    async def add_book(data,session:AsyncSession):

        try:
            print(f"++here is the error 3")
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return data
           
        except Exception as e:
            await session.rollback()
            print(f"error in adding data: {e}")
            raise 
