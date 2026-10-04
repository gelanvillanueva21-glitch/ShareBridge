# backend/app/repositories/message_repository.py
"""Message repository for direct‑message persistence.
Provides async CRUD utilities used by the WebSocket router and any
future HTTP endpoints.
"""

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.exceptions import NotFoundError


class MessageRepository:
    """Repository layer for the Message model.
    All DB interaction is kept here so higher layers stay thin.
    """

    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(
        self,
        sender_id: int,
        receiver_id: int,
        content: str | None = None,
        emoji: str | None = None,
        photo_id: int | None = None,
        donation_id: int | None = None,
    ) -> Message:
        """Insert a new Message and return the ORM instance.
        The returned object already contains the generated primary key.
        """
        stmt = insert(Message).values(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            emoji=emoji,
            photo_id=photo_id,
            donation_id=donation_id,
        ).returning(Message)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()


    async def get_by_id(self, message_id: int) -> Message | None:
        stmt = select(Message).where(Message.id == message_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_conversation(
        self,
        sender_id: int,
        receiver_id: int,
        limit: int = 50,
        offset: int = 0,
        last_message_id: int | None = None,
    ) -> list[Message]:
        """Return up‑to‑`limit` messages exchanged between two users.
        Ordered newest‑first; `offset` can be used for pagination.
        If `last_message_id` is supplied, only messages with an id **less**
        than that value are returned – useful for infinite‑scroll "load older"
        scenarios where the client sends the oldest message it currently has.
        """
        base_condition = (
            ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id))
            | ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
        )
        if last_message_id is not None:
            # fetch messages older than the provided id
            condition = base_condition & (Message.id < last_message_id)
        else:
            condition = base_condition
        stmt = (
            select(Message)
            .where(condition)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def get_unread_by_user(self, user_id: int) -> list[Message]:
        stmt = select(Message).where(
            Message.receiver_id == user_id,
            Message.is_read == False,
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def mark_as_read(self, message_id: int) -> None:
        stmt = (
            update(Message)
            .where(Message.id == message_id)
            .values(is_read=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()


    async def delete(self, message_id: int) -> None:
        result = await self.db.execute(select(Message).where(Message.id == message_id))
        message = result.scalar_one_or_none()
        if message is None:
            raise NotFoundError(f"Message with id {message_id} not found")

        await self.db.delete(message)
        await self.db.commit()
