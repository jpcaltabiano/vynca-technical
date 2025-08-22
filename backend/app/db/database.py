import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DB_URL = "sqlite+aiosqlite:///./app.db"

# entry point
engine = create_async_engine(DB_URL, echo=True)

# session maker
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# base class
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session