from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, JSON, Uuid,DateTime,func,Column
import uuid
from datetime import datetime



class Base(DeclarativeBase):
    pass




class User(Base):
    __tablename__ = "Users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    name:Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone:Mapped[str] = mapped_column(String(), default="+91-999999999") # neeed typing chgecking accourding the internatinal numbers
    password: Mapped[str] = mapped_column(String, nullable=False)
    book_list: Mapped[list] = mapped_column(JSON,default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )          

    def __repr__(self):
        return f"<Users {self.name}>"                                        



class UserCreateModel(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    book_list:list[str]