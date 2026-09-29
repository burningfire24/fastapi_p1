from pydantic import BaseModel,Field
import uuid   
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import JSON, String, Uuid, DateTime, func,Integer

from datetime import datetime, date

from src.db.schema import Base


class Book(Base):
    __tablename__="Book"

    uid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    Title:Mapped[str]=mapped_column(String,nullable=False)
    Author:Mapped[str]=mapped_column(String,nullable=False)
    publisher:Mapped[str]=mapped_column(String,nullable=False)
    published_year:Mapped[datetime] = mapped_column(DateTime)
    ISBN :Mapped[str] = mapped_column(String, nullable=False) #(International Standard Book Number): A unique 10-digit or 13-digit 
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )   

    def __repr__(self):
        return f"<Book {self.Title}>"



class CreateModel(BaseModel):
    Title:str = Field(..., min_length=1)
    Author:str = Field(..., min_length=1)
    publisher:str = Field(..., min_length=1)
    published_year:date
    ISBN: str = Field(..., pattern=r"^\d{10}(\d{3})?$")


class BookReadModel(BaseModel):
    Titel:str
    Author:str
    publisher:str
    published_year:datetime
    ISBN:int

class BookCreateModelDB(BaseModel):
    pass

class ReadRequest(BaseModel):
    pass