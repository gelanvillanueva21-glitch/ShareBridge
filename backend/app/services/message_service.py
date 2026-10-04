# backend/app/services/message_service.py
"""Message service – business logic for the direct‑messaging feature.
All operations that involve validation, permission checks, or orchestration
between multiple repositories belong here. Routers (HTTP or WebSocket) will
inject this service via FastAPI's Depends().
"""

from typing import List

from app.exceptions import NotFoundError, PermissionDeniedError
from app.models.message import Message
from app.schemas.message import MessageRead
from app.models.photo import Photo, PhotoPurpose
from app.models.user import UserRole

# Repository imports (these are FastAPI dependencies that will be injected
# elsewhere – the service receives concrete instances).
from app.utils.repositories import get_message_repository
from app.utils.repositories import get_user_repository
from app.utils.repositories import get_profile_repository

# The utils package provides a Database session dependency, but the service
# receives repositories directly, so we only import the repository classes
# for type‑checking.
from app.repositories.message_repository import MessageRepository
from app.repositories.photo_repository import PhotoRepository
from app.repositories.user_repository import UserRepository


class MessageService:
    """Business‑logic layer for messaging.
    It validates input, enforces domain rules, and delegates persistence to
    the repository layer.
    """

    def __init__(
        self,
        msg_repo: MessageRepository,
        user_repo: UserRepository,
        photo_repo: PhotoRepository,
    ) -> None:
        self.msg_repo = msg_repo
        self.user_repo = user_repo
        self.photo_repo = photo_repo


    async def _ensure_user_exists(self, user_id: int) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")


    async def _ensure_photo_is_private_message(self, photo_id: int) -> None:
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise NotFoundError(f"Photo with id {photo_id} not found")
        if photo.purpose != PhotoPurpose.PRIVATE_MESSAGE:
            raise PermissionDeniedError(
                "Only photos with purpose PRIVATE_MESSAGE may be attached to a direct message"
            )


    async def send_message(
        self,
        sender_id: int,
        receiver_id: int,
        content: str | None = None,
        image_url: str | None = None,
        emoji: str | None = None,
        donation_id: int | None = None,
    ) -> MessageRead:
        """Create a new message after performing business‑level checks.
        Returns a Pydantic `MessageRead` ready for serialization.
        """
        # Basic sanity checks
        if sender_id == receiver_id:
            raise PermissionDeniedError("Cannot send a message to yourself")
        await self._ensure_user_exists(sender_id)
        await self._ensure_user_exists(receiver_id)

        result = None
        if image_url:
            result = await self.photo_repo.create_photo(
                sender_id, 
                image_url, 
                PhotoPurpose.PRIVATE_MESSAGE
            )
            await self._ensure_photo_is_private_message(result.id)
        msg: Message = await self.msg_repo.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            emoji=emoji,
            photo_id=result.id if result else None,
            donation_id=donation_id,
        )

        return MessageRead.model_validate(msg)


    async def get_conversation(
        self,
        sender_id: int,
        receiver_id: int,
        last_message_id: int | None = None,
    ) -> List[MessageRead]:
        """Fetch a paginated slice of a conversation.
        `last_message_id` is used for "load older" scrolling – only messages
        with an id smaller than that value are returned.
        """
        await self._ensure_user_exists(sender_id)
        await self._ensure_user_exists(receiver_id)
        msgs: List[Message] = await self.msg_repo.get_conversation(
            sender_id=sender_id,
            receiver_id=receiver_id,
            limit=50,
            offset=0,
            last_message_id=last_message_id,
        )
        return [MessageRead.model_validate(m) for m in msgs]


    async def get_unread(self, user_id: int) -> List[MessageRead]:
        """Return all unread messages for a given user."""
        await self._ensure_user_exists(user_id)
        msgs = await self.msg_repo.get_unread_by_user(user_id)
        return [MessageRead.model_validate(m) for m in msgs]


    async def mark_as_read(self, message_id: int, user_id: int) -> None:
        """Mark a message as read – only the receiver may perform this.
        Raises `PermissionDeniedError` if the user is not the intended
        recipient, and `NotFoundError` if the message does not exist.
        """
        msg: Message | None = await self.msg_repo.get_by_id(message_id)
        if not msg:
            raise NotFoundError(f"Message with id {message_id} not found")
        if msg.receiver_id != user_id:
            raise PermissionDeniedError("Only the message recipient can mark it as read")
        await self.msg_repo.mark_as_read(message_id)


    async def delete_message(
            self, 
            message_id: int, 
            requester_id: int
        ) -> None:
        """
        Delete a message. Allowed for the sender or an admin.
        This method is not required for the current feature set but is
        provided for future admin tools.
        """
        msg = await self.msg_repo.get_by_id(message_id)
        account = await self.user_repo.get_by_id(requester_id)

        if not account:
            raise NotFoundError(f"User with id {requester_id} not found")
        if not msg:
            raise NotFoundError(f"Message with id {message_id} not found")
        if msg.sender_id != requester_id and account.role != UserRole.ADMIN:
            raise PermissionDeniedError("Only the sender or an admin can delete a message")
        await self.msg_repo.delete(message_id)
