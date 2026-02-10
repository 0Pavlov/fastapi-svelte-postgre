# The api
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# Data validation and schema definition
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated, Optional, AsyncGenerator
from enum import IntEnum

# Custom modules
from database import engine, Base, AsyncSessionLocal
from models import TodoDB
from schemas import (
        TodoCreate,
        TodoUpdate,
        TodoResponse,
        Priority
)
from dependencies import get_db

from contextlib import asynccontextmanager
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# Lifespan (startup and shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code before 'yield' runs when the server starts.
    Code after 'yield' runs when the server stops.
    """
    print("Starting up... Checking Database...")
    
    # Create Tables
    # This creates tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create Sample Data (if empty)
    async with AsyncSessionLocal() as session:
        # Check count of rows
        result = await session.execute(select(func.count()).select_from(TodoDB))
        if result.scalar() == 0:
            print("Database empty. Seeding sample data...")
            sample_todos = [
                TodoDB(name="Test task", description="Test description", priority=1),
            ]
            session.add_all(sample_todos)
            await session.commit()
    
    print("System Ready.")

    # The application runs while looking at this point
    yield
    
    print("Shutting down... Closing Database connection.")
    await engine.dispose()

# The app
app = FastAPI(
    title="Todo API",
    description="A FastAPI and Postgres async backend",
    lifespan=lifespan
)

# CORS configuration to allow frontend talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be changed in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# A health endpoint
@app.get("/", tags=["Health"])
async def index():
    """Simple health check endpoint."""
    return {"status": "Backend is running"}

# Get all todos
@app.get("/todos", response_model=List[TodoResponse], tags=["Todos"])
async def get_todos(
        first_n: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    """Fetch all or first_n todos."""
    # Build the query
    # Select all todos ordered by ids
    query = select(TodoDB).order_by(TodoDB.id)

    if first_n:
        # Limit by n if the first_n is present
        query = query.limit(first_n)

    # Execute query (async)
    # await pauses here until DB responds
    result = await db.execute(query)

    # Extract Python objects from the result
    todos_db = result.scalars().all()

    # Conversion to Pydantic
    # I have set 'from_attributes=True' in TodoResponse, so if the field names match,
    # I can let Pydantic handle it
    # return [TodoResponse.model_validate(todo) for todo in todos_db]

    # Here is the manual mapping to show explicitly what happens
    return [
        TodoResponse(
            todo_id=todo.id,
            todo_name=todo.name,
            todo_description=todo.description,
            todo_priority=Priority(todo.priority) # Convert int to Enum
        ) for todo in todos_db
    ]
