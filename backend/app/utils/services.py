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
from app.repositories.photo_repository import PhotoRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.volunteer_repository import VolunteerRepository
from .repositories import (
    get_user_repository, 
    get_profile_repository, 
    get_message_repository, 
    get_photo_repository,
    get_volunteer_repository
)


# Import service classes
from app.services.message_service import MessageService
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.services.claim_service import ClaimService


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
        repo: Annotated[ProfileRepository, Depends(
            get_profile_repository
        )],
        photo_repo: Annotated[PhotoRepository, Depends(
            get_photo_repository
        )]
    ) -> ProfileService:
    """Create a `ProfileService` bound to the current DB session and repository."""
    return ProfileService(db, repo, photo_repo)


def get_message_service(
    msg_repo: Annotated[MessageRepository, Depends(get_message_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    photo_repo: Annotated[PhotoRepository, Depends(get_photo_repository)],
) -> MessageService:
    """Create a `MessageService` bound to the current DB session and repositories."""
    return MessageService(msg_repo, user_repo, photo_repo)


def get_claim_service(
    db: DatabaseDepends,
    repo: Annotated[VolunteerRepository, Depends(get_volunteer_repository)],
    photo_repo: Annotated[PhotoRepository, Depends(get_photo_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> ClaimService:
    """Create a `ClaimService` bound to the current repositories."""
    return ClaimService(db, repo, photo_repo, user_repo)

