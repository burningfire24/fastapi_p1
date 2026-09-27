from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.db.schema import Base, User

from src.db.database import engine
from src.usersely.Router import user_router




@asynccontextmanager
async def life_span(app:FastAPI):
    #start
    print("server is running")
    async with engine.begin() as conn:
        print("Database connection successful")
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    #end
    print("server has been stoped")
    await engine.dispose()

version = "v1"

app=FastAPI(
    title="userely",
    description="creating user manager REST api",
    version=version,
    lifespan = life_span
)


app.include_router(user_router, prefix=f"/api/{version}/users",tags=['Users'])
