from pydantic import BaseModel
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import JSON, String, Uuid, DateTime, func,Integer

from datetime import datetime

from src.db.schema import Base


class Book(Base):
    __tablename__="Book"

    uid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    Title:Mapped[str]=mapped_column(String,nullable=False)
    Author:Mapped[str]=mapped_column(String,nullable=False)
    publisher:Mapped[str]=mapped_column(String,nullable=False)
    published_year:Mapped[datetime] = mapped_column(DateTime)
    ISBN :Mapped[int]=mapped_column(Integer,nullable=False) #(International Standard Book Number): A unique 10-digit or 13-digit 
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