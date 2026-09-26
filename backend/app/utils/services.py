# backend/app/utils/services.py
"""Factory functions and Annotated shortcuts for all service classes.
Each function receives a `DbSession` and the appropriate repository instance,
instantiating the service with those dependencies.  The annotated variables are
exported for direct injection in routers.
"""

from typing import Annotated
from .db_session import DbSession
from .repositories import UserRepo, ProfileRepo

# Import service classes
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
# Add other service imports here as they are created.


def get_user_service(db: DbSession, repo: UserRepo) -> UserService:
    """Create a `UserService` bound to the current DB session and repository."""
    return UserService(db, repo)


def get_profile_service(db: DbSession, repo: ProfileRepo) -> ProfileService:
    """Create a `ProfileService` bound to the current DB session and repository."""
    return ProfileService(db, repo)

