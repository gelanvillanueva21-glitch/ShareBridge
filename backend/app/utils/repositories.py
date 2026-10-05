# backend/app/utils/repositories.py
"""Factory functions and Annotated shortcuts for all repository classes.
Each function receives a `DatabaseDepends` (the async SQLAlchemy session) and returns the
corresponding repository instance.  The annotated variables are exported for
direct reuse in routers and services.
"""


from fastapi import Depends
from .db_session import DatabaseDepends

# Import repository classes
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.photo_repository import PhotoRepository
from app.repositories.volunteer_repository import VolunteerRepository
# Add other repositories here as they appear in the project.



def get_user_repository(db: DatabaseDepends) -> UserRepository:
    """Create a `UserRepository` bound to the current DB session."""
    return UserRepository(db)


def get_profile_repository(db: DatabaseDepends) -> ProfileRepository:
    """Create a `ProfileRepository` bound to the current DB session."""
    return ProfileRepository(db)


def get_message_repository(db: DatabaseDepends) -> MessageRepository:
    """Create a `MessageRepository` bound to the current DB session."""
    return MessageRepository(db)


def get_photo_repository(db: DatabaseDepends) -> PhotoRepository:
    """Create a `PhotoRepository` bound to the current DB session."""
    return PhotoRepository(db)



def get_volunteer_repository(db: DatabaseDepends) -> VolunteerRepository:
    """Create a `VolunteerRepository` bound to the current DB session."""
    return VolunteerRepository(db)
