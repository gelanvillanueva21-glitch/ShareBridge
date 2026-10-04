from pydantic import BaseModel, ConfigDict
from datetime import datetime



class MessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

