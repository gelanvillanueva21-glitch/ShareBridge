# backend/app/utils/db_session.py
"""Database session dependency.
Provides the root async session and a reusable Annotated variable.
"""

from typing import Annotated, TypeAlias
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal

async def get_db():
    """Yield a single AsyncSession per request and close it after use."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Annotated shortcut for any component needing the Database session.
DatabaseDepends: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
