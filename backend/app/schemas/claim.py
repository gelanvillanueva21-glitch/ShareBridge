from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.claim import ClaimStatus

class ClaimBase(BaseModel):
    donation_id: int

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    status: Optional[ClaimStatus] = None
    delivery_caption: Optional[str] = None

class ClaimRead(ClaimBase):
    id: int
    volunteer_id: int
    status: ClaimStatus
    delivery_caption: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
