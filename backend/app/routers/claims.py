"""HTTP endpoints for volunteer donation claims."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.exceptions import (
    AlreadyExistsError,
    AppError,
    NotFoundError,
    PermissionDeniedError,
)
from app.models.claim import ClaimStatus
from app.models.user import User, UserRole
from app.schemas.claim import ClaimCreate, ClaimRead
from app.utils.dependencies import ClaimServiceDep, CurrentUser

router = APIRouter(prefix="/claims", tags=["Claims"])


def _http_exception(error: AppError) -> HTTPException:
    if isinstance(error, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(error, PermissionDeniedError):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(error, AlreadyExistsError):
        status_code = status.HTTP_409_CONFLICT
    else:
        status_code = status.HTTP_400_BAD_REQUEST
    return HTTPException(
        status_code=status_code, 
        detail=error.message
    )


def _require_volunteer(current_user: User) -> None:
    if current_user.role != UserRole.VOLUNTEER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only volunteers can manage claims.",
        )


@router.post(
    "",
    response_model=ClaimRead,
    status_code=status.HTTP_201_CREATED,
)
async def request_claim(
    payload: ClaimCreate,
    service: ClaimServiceDep,
    current_user: CurrentUser,
) -> ClaimRead:
    """Create a claim for a donation as the authenticated volunteer."""
    _require_volunteer(current_user)
    try:
        return await service.request_claim(
            volunteer_id=current_user.id,
            donation_id=payload.donation_id,
        )
    except AppError as error:
        raise _http_exception(error) from error


@router.post(
    "/{donation_id}/status",
    response_model=ClaimRead,
)
async def update_claim_status(
    donation_id: int,
    service: ClaimServiceDep,
    current_user: CurrentUser,
    new_status: ClaimStatus = Form(...),
    proof_image: UploadFile | None = File(default=None),
) -> ClaimRead:
    """Update this volunteer's claim status and optionally attach completion proof."""
    _require_volunteer(current_user)
    try:
        return await service.update_claim_status(
            volunteer_id=current_user.id,
            donation_id=donation_id,
            new_status=new_status,
            proof_image=proof_image,
        )
    except AppError as error:
        raise _http_exception(error) from error


