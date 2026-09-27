from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import config


engine = create_async_engine(
    config.DATABASE_URL.get_secret_value(),
    echo=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, 
)


async def db_connection():
    async with async_session() as session:
        try:
            yield session
            print("DB connection successful")
        except Exception as e:
            print(f"Failed to connect with error: {e}")
            await session.rollback()