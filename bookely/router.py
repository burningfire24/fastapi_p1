from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

#same Folder
from .services import BookService
from .schema import BookReadModel,CreateModel,Book


#other folders
from src.db.database import db_connection


router_book = APIRouter()
user_service = BookService()

@router_book.post('/add_book') #,response_model=BookReadModel)
async def add_book(book_data:CreateModel,db_session:AsyncSession = Depends(db_connection)):

    try:
        #check if the book is present or not
        
        query_result = await BookService.get_book_name_search(book_data.Title,db_session)
       
        if query_result is None:
            new_book = Book(**book_data.model_dump())
            result = await BookService.add_book(new_book,db_session)
            return result

        #if not then add and return book data
        else:
            return query_result
            
    except Exception as e:
        raise HTTPException(status_code=301, detail=str(f"Error:{e}"))        
    pass


@router_book.get('/get_book/{book_id}')
async def get_book(book_id:UUID,db_session:AsyncSession = Depends(db_connection)):
    
        book = await BookService.get_book_by_uid(book_id,db_session)
        if book == None:
            raise HTTPException(status_code=302, detail=str("book not found")) 
        else:
            return book