from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import IntEnum

# Pydantic models/schemas
# These classes define the JSON shape expected by the API 
# (I/O)
# They act as a filter/validation layer before data touches
# the logic or database

class Priority(IntEnum):
    """
    Priority of the task.
    Enum to ensure priority is always a specific set of
    numbers.
    """
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    """Shared properties for creating or reading todos."""
    todo_name: str = Field(
        ...,
        min_length=3,
        max_length=512,
        description="Title"
    )
    todo_description: str = Field(
        ...,
        description="Details"
    )
    todo_priority: Priority = Field(
        default=Priority.LOW,
        description="1=High, 2=Med, 3=Low"
    )

class TodoCreate(TodoBase):
    """
    Schema for receiving data from a client (POST request).
    """
    # Inherits everything from TodoBase 
    # We don't need 'id' here because the database 
    # generates it
    pass

class TodoUpdate(BaseModel):
    """
    Schema for updating (PUT request).
    All fields are optional.
    """
    todo_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=512
    )
    todo_description: Optional[str] = Field(None)
    todo_priority: Optional[Priority] = Field(None)

class TodoResponse(TodoBase):
    """Schema for sending data back to the client."""
    # The DB ID is required when sending data back
    todo_id: int 
    # ConfigDict tells Pydantic: 
    # "It's okay to read data from a non-JSON object 
    # (like a SQLAlchemy database model) 
    # and convert it to JSON"
    model_config = ConfigDict(from_attributes=True)

