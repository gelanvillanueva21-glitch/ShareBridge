# backend/app/utils/repositories.py
"""Factory functions and Annotated shortcuts for all repository classes.
Each function receives a `DbSession` (the async SQLAlchemy session) and returns the
corresponding repository instance.  The annotated variables are exported for
direct reuse in routers and services.
"""

from typing import Annotated
from fastapi import Depends
from .db_session import DbSession

# Import repository classes
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
# Add other repositories here as they appear in the project.


def get_user_repository(db: DbSession) -> UserRepository:
    """Create a `UserRepository` bound to the current DB session."""
    return UserRepository(db)


def get_profile_repository(db: DbSession) -> ProfileRepository:
    """Create a `ProfileRepository` bound to the current DB session."""
    return ProfileRepository(db)

