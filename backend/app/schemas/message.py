from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class MessageBase(BaseModel):
    receiver_id: int = Field(gt=0)
    content: str | None = None
    emoji: str | None = None
    donation_id: int | None = Field(default=None, gt=0)


class MessageCreate(MessageBase):
    """Request schema for sending a direct message."""


class MessageRead(BaseModel):
    """Response schema for a message.

    Includes the full message body (content, emoji, photo reference)
    so the client can render a complete chat bubble — just like a
    typical messenger app.
    """
    id: int
    sender_id: int
    receiver_id: int
    content: str | None = None
    emoji: str | None = None
    photo_id: int | None = None
    image_url: str | None = None
    donation_id: int | None = None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
