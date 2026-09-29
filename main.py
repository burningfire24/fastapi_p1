from fastapi import FastAPI
# from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.db.schema import Base, User

from src.db.database import engine
from src.usersely.Router import user_router
from bookely.router import router_book

#NOT REQUIRED AS THE ALEMBIC IS MANAGING IT
# @asynccontextmanager
# async def life_span(app:FastAPI):
#     #start
#     print("server is running")
#     async with engine.begin() as conn:
#         print("Database connection successful")
#         await conn.run_sync(Base.metadata.create_all)
    
#     yield

#     #end
#     print("server has been stoped")
#     await engine.dispose()

version = "v1"

app=FastAPI(
    title="userely",
    description="creating user manager REST api",
    version=version,
    #lifespan = life_span
)

##############################################validation cataching######################################
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

########################################################################################################


app.include_router(user_router, prefix=f"/api/{version}/users",tags=['Users'])
app.include_router(router_book, prefix=f"/api/{version}/book",tags=['Books'])
