# backend/app/utils/services.py
"""Factory functions and Annotated shortcuts for all service classes.
Each function receives a `DatabaseDepends` session and the appropriate repository
instance, then creates the service.  The exported shortcuts are declared as
`TypeAlias` so they can be used directly in FastAPI endpoint signatures.
"""


from fastapi import Depends
from .db_session import DatabaseDepends
from .repositories import UserRepositoryDepends, ProfileRepositoryDepends

# Import service classes
from app.services.user_service import UserService
from app.services.profile_service import ProfileService


def get_user_service(db: DatabaseDepends, repo: UserRepositoryDepends) -> UserService:
    """Create a `UserService` bound to the current DB session and repository."""
    return UserService(db, repo)


def get_profile_service(db: DatabaseDepends, repo: ProfileRepositoryDepends) -> ProfileService:
    """Create a `ProfileService` bound to the current DB session and repository."""
    return ProfileService(db, repo)


