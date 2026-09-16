from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    receiver_id: int
    donation_id: Optional[int] = None
    content: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    sender_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

