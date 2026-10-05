# backend/app/utils/dependencies.py
"""Core dependencies for the ShareBridge backend.
Provides:
* `DbSession` – async DB session (from utils.db_session).
* Auth helpers (`get_current_user`, `get_current_admin`).
* Annotated shortcuts for repositories and services – imported from the
  dedicated `utils.repositories` and `utils.services` modules.
"""

from typing import Annotated, TypeAlias

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError

from .repositories import ( 
    get_profile_repository, 
    get_user_repository, 
    get_message_repository,
    get_photo_repository,
    get_volunteer_repository
)

from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.photo_repository import PhotoRepository
from app.repositories.volunteer_repository import VolunteerRepository
from app.utils.security import decode_token

from .services import (
    get_profile_service,
    get_user_service,
    get_message_service,
    get_claim_service,
)
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.services.message_service import MessageService
from app.services.claim_service import ClaimService

# Service Dependencies Reusable Variable

UserServiceDep: TypeAlias = Annotated[UserService, Depends(get_user_service)]
ProfileServiceDep: TypeAlias = Annotated[ProfileService, Depends(get_profile_service)]
MessageServiceDep: TypeAlias = Annotated[MessageService, Depends(get_message_service)]
ClaimServiceDep: TypeAlias = Annotated[ClaimService, Depends(get_claim_service)]

# Repository Dependencies Reusable Variable

UserRepo: TypeAlias = Annotated[UserRepository, Depends(get_user_repository)]
ProfileRepo: TypeAlias = Annotated[ProfileRepository, Depends(get_profile_repository)]
VolunteerRepo: TypeAlias = Annotated[VolunteerRepository, Depends(get_volunteer_repository)]
PhotoRepo: TypeAlias = Annotated[PhotoRepository, Depends(get_photo_repository)]
MessageRepo: TypeAlias = Annotated[MessageRepository, Depends(get_message_repository)]


# Authentication Guard whenver the user fetching data
# Checking aswell if jwt is exist in the cookie



async def get_current_user(
    request: Request,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """Validate the JWT access token and fetch the corresponding User.
    Directly uses the repository to avoid an extra service layer.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise credentials_exception
    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user



# Dependencies for getting the currentuser data
CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]



async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require the authenticated user to have the ADMIN role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user



# Dependencies for getting the current admin data
CurrentAdmin: TypeAlias = Annotated[User, Depends(get_current_admin)]
