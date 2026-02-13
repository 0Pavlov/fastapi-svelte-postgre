from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase

# Connection String
# protocol+driver://username:password@host:port/database_name
# Use postgresql for the protocol and asyncpg driver
# asyncpg is a very fast async driver for Python
# Use this url if running all manually
#DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/todo_db"
# Use this url if running with docker
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/todo_db"

# Engine
# The entry point to the database
# echo=True prints the actual SQL queries to the console 
engine = create_async_engine(DATABASE_URL, echo=True)

# Session Factory
# Creates new database sessions for each request
# expire_on_commit=False prevents objects from 
# detaching after we save them, which is required 
# for async operations
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base Class 
# All database models (tables) will inherit from this
# It handles the mapping between Python classes and 
# SQL tables
class Base(AsyncAttrs, DeclarativeBase):
    pass

