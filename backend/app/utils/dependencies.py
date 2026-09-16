from typing import Annotated

from fastapi import Depends, HTTPException, status, Request, Cookie
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.utils.security import decode_token
from app.exceptions import InvalidTokenError


# ---------------------------------------------------------------------------
# Database Session
# ---------------------------------------------------------------------------

async def get_db() -> AsyncSession:
    """
    Yields one AsyncSession per request, closes it automatically after.
    This is the root dependency everything else builds on.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ---------------------------------------------------------------------------
# Repository Factories
# ---------------------------------------------------------------------------

def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """Creates a UserRepository with the current request's DB session."""
    return UserRepository(db)


# ---------------------------------------------------------------------------
# Service Factories
# ---------------------------------------------------------------------------

def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Creates a UserService with the DB session and UserRepository injected."""
    return UserService(db, repo)


# ---------------------------------------------------------------------------
# Auth Guard
# ---------------------------------------------------------------------------

async def get_current_user(
    request: Request,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """
    Reads and validates the Access Token from the Authorization header.
    Returns the full User object from the database.
    Uses the repository directly — no need to go through the service.
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


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Extends get_current_user — additionally checks the Admin role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user


# ---------------------------------------------------------------------------
# Pre-built Annotated Dependency Variables
# Write these ONCE here, use them anywhere without repeating Annotated syntax.
# ---------------------------------------------------------------------------

DbSession = Annotated[AsyncSession, Depends(get_db)]
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
