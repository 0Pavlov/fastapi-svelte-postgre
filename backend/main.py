# The api
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# Data validation and schema definition
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated, Optional, AsyncGenerator

# The app
app = FastAPI(
    title="Todo API",
    description="A FastAPI and Postgres async backend",
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
