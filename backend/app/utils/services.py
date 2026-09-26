# backend/app/utils/services.py
"""Factory functions and Annotated shortcuts for all service classes.
Each function receives a `DatabaseDepends` session and the appropriate repository
instance, then creates the service.  The exported shortcuts are declared as
`TypeAlias` so they can be used directly in FastAPI endpoint signatures.
"""


from typing import Annotated
from fastapi import Depends
from .db_session import DatabaseDepends
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from .repositories import get_user_repository, get_profile_repository


# Import service classes
from app.services.user_service import UserService
from app.services.profile_service import ProfileService


def get_user_service(
        db: DatabaseDepends, 
        repo: Annotated[UserRepository, Depends(
            get_user_repository
        )]
    ) -> UserService:
    """Create a `UserService` bound to the current DB session and repository."""
    return UserService(db, repo)


def get_profile_service(
        db: DatabaseDepends, 
        repo: Annotated[ProfileService, Depends(
            get_profile_repository
        )]
    ) -> ProfileService:
    """Create a `ProfileService` bound to the current DB session and repository."""
    return ProfileService(db, repo)


