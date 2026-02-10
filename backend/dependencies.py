from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    This function handles the database session lifecycle.
    Opens a session.
    'yields' it to the endpoint function 
    (endpoint runs here)
    Closes the session automatically after the endpoint 
    finishes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Commit inside the endpoint,
            # but just in case, close cleanly
        except Exception:
            # If error, undo any partial DB changes
            await session.rollback()
            raise
        finally:
            # Always close the connection
            await session.close()

