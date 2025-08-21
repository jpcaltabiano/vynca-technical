import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DB_URL = "sqlite+aiosqlite:///./app.db"

# entry point
engine = create_async_engine(DB_URL, echo=True)

# session maker
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# base class
Base = declarative_base()