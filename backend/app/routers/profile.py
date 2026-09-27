# backend/app/routers/profile.py
"""Profile router – handles profile‑related actions.
All endpoints follow the same error‑handling pattern as `routers/users.py`:
* Business‑logic errors are raised as custom exceptions in the service layer.
* The router catches those exceptions and maps them to appropriate `HTTPException`
responses.
* Unexpected errors are turned into a generic 500 response.
"""

import logging
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query

from app.exceptions import AppError
from app.utils.dependencies import CurrentUser, ProfileServiceDep
from app.schemas.profile import ProfileRead, ProfileUpdate, ProfileSearchResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileRead)
async def read_my_profile(
    service: ProfileServiceDep,
    current_user: CurrentUser,
) -> ProfileRead:
    """Return the current user's profile (creates a default one if missing)."""
    try:
        return await service.get_my_profile(current_user)
    except AppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        logger.exception("Unexpected error while reading current profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        )


@router.patch("/me", response_model=ProfileRead)
async def update_my_profile(
    payload: ProfileUpdate,
    service: ProfileServiceDep,
    current_user: CurrentUser,
) -> ProfileRead:
    """Partially update the current user's profile fields."""
    try:
        return await service.update_my_profile(payload, current_user)
    except AppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        logger.exception("Unexpected error while updating current profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        )


@router.post("/photo", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def upload_profile_photo(
    service: ProfileServiceDep,
    current_user: CurrentUser,
    file: UploadFile = File(...),
) -> ProfileRead:
    """Upload a new profile picture and attach it to the user's profile."""
    try:
        return await service.upload_profile_photo(file, current_user)
    except AppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        logger.exception("Unexpected error while uploading profile photo")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        )


@router.get("/search", response_model=list[ProfileSearchResult])
async def search_profiles(
    service: ProfileServiceDep,
    query: str = Query(..., min_length=1, description="Search by profile name, city, or bio (for example: Ge)"),
    city: str | None = Query(None, description="Optional city filter"),
) -> list[ProfileSearchResult]:
    """Search public profiles by text. Keeps the API simple for frontend use."""
    try:
        return await service.search_profiles(
            query=query,
            city=city,
        )
    except AppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        logger.exception("Unexpected error while searching profiles")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        )
