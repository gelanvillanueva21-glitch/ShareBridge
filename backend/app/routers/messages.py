"""HTTP endpoints for direct messages."""

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.exceptions import AppError, NotFoundError, PermissionDeniedError
from app.schemas.message import MessageCreate, MessageRead
from app.utils.dependencies import CurrentUser, MessageServiceDep

router = APIRouter(prefix="/messages", tags=["Messages"])


def _http_exception(error: AppError) -> HTTPException:
    if isinstance(error, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(error, PermissionDeniedError):
        status_code = status.HTTP_403_FORBIDDEN
    else:
        status_code = status.HTTP_400_BAD_REQUEST
    return HTTPException(status_code=status_code, detail=error.message)


@router.post(
    "",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    payload: MessageCreate,
    service: MessageServiceDep,
    current_user: CurrentUser,
) -> MessageRead:
    """Send a message to another user."""
    try:
        return await service.send_message(
            sender_id=current_user.id,
            receiver_id=payload.receiver_id,
            content=payload.content,
            image_url=payload.image_url,
            emoji=payload.emoji,
            donation_id=payload.donation_id,
        )
    except AppError as error:
        raise _http_exception(error) from error


@router.get(
    "/conversation/{other_user_id}",
    response_model=list[MessageRead],
)
async def get_conversation(
    other_user_id: int,
    service: MessageServiceDep,
    current_user: CurrentUser,
    last_message_id: int | None = Query(default=None, gt=0),
) -> list[MessageRead]:
    """Get the authenticated user's conversation with another user."""
    try:
        return await service.get_conversation(
            sender_id=current_user.id,
            receiver_id=other_user_id,
            last_message_id=last_message_id,
        )
    except AppError as error:
        raise _http_exception(error) from error


@router.get("/unread", response_model=list[MessageRead])
async def get_unread_messages(
    service: MessageServiceDep,
    current_user: CurrentUser,
) -> list[MessageRead]:
    """Get unread messages addressed to the authenticated user."""
    try:
        return await service.get_unread(user_id=current_user.id)
    except AppError as error:
        raise _http_exception(error) from error


@router.patch("/{message_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_message_as_read(
    message_id: int,
    service: MessageServiceDep,
    current_user: CurrentUser,
) -> Response:
    """Mark a message as read; only its recipient may do so."""
    try:
        await service.mark_as_read(message_id=message_id, user_id=current_user.id)
    except AppError as error:
        raise _http_exception(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    service: MessageServiceDep,
    current_user: CurrentUser,
) -> Response:
    """Delete a message as its sender or an admin."""
    try:
        await service.delete_message(
            message_id=message_id,
            requester_id=current_user.id,
        )
    except AppError as error:
        raise _http_exception(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


