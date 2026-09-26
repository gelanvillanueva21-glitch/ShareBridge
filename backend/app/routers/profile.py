# backend/app/routers/profile.py
"""Profile router – handles profile‑related actions.
All endpoints follow the same error‑handling pattern as `routers/users.py`:
* Business‑logic errors are raised as custom exceptions in the service layer.
* The router catches those exceptions and maps them to appropriate `HTTPException`
  responses.
* Unexpected errors are turned into a generic 500 response.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File

from app.utils.dependencies import CurrentUser, ProfileServiceDep
from app.schemas.profile import ProfileRead, ProfileUpdate


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileRead)
async def read_my_profile(
    service: ProfileServiceDep,
    current_user: CurrentUser,
) -> ProfileRead:
    """Return the current user's profile (creates a default one if missing)."""
    try:
        return await service.get_my_profile(current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        ) from e


@router.patch("/me", response_model=ProfileRead)
async def update_my_profile(
    payload: ProfileUpdate,
    service: ProfileServiceDep,
    current_user: CurrentUser,
) -> ProfileRead:
    """Partially update the current user's profile fields."""
    try:
        return await service.update_my_profile(payload, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        ) from e


@router.post("/photo", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def upload_profile_photo(
    service: ProfileServiceDep,
    current_user: CurrentUser,
    file: UploadFile = File(...),
) -> ProfileRead:
    """Upload a new profile picture and attach it to the user's profile."""
    try:
        return await service.upload_profile_photo(file, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        ) from e

