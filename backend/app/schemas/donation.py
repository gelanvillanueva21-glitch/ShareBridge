from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.donation import DonationCategory, UrgencyLevel, ItemCondition

class DonationBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: DonationCategory
    quantity: str
    condition: ItemCondition
    is_perishable: bool = False
    urgency: UrgencyLevel = UrgencyLevel.LOW
    pickup_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    availability_window: Optional[str] = None
    notes: Optional[str] = None

class DonationCreate(DonationBase):
    pass

class DonationUpdate(BaseModel):
    is_claimed: Optional[bool] = None
    is_completed: Optional[bool] = None

class DonationRead(DonationBase):
    id: int
    donor_id: int
    is_claimed: bool
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
