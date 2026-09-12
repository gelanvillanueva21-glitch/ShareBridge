from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Create async engine for PostgreSQL
engine = create_async_engine(settings.database_url, echo=True)

# Create session maker
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class for all models
Base = declarative_base()
