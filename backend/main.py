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
