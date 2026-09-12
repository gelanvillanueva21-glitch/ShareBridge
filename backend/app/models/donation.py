import enum
from datetime import datetime
from sqlalchemy import String, Float, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class DonationCategory(str, enum.Enum):
    FOOD = "food"
    CLOTHING = "clothing"
    BOOKS = "books"
    FURNITURE = "furniture"
    ELECTRONICS = "electronics"
    HYGIENE = "hygiene"
    OTHER = "other"

class UrgencyLevel(str, enum.Enum):
    HIGH = "high"       # e.g., expires in hours (Red)
    MEDIUM = "medium"   # e.g., expires today (Green)
    LOW = "low"         # e.g., non-perishable

class ItemCondition(str, enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class Donation(Base):
    """
    Represents an item posted by a Donor.
    """
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    donor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[DonationCategory] = mapped_column(Enum(DonationCategory), nullable=False)
    quantity: Mapped[str] = mapped_column(String, nullable=False) # e.g., "3 boxes", "5 kg"
    condition: Mapped[ItemCondition] = mapped_column(Enum(ItemCondition), nullable=False)
    
    # Perishables & Urgency
    is_perishable: Mapped[bool] = mapped_column(Boolean, default=False)
    urgency: Mapped[UrgencyLevel] = mapped_column(Enum(UrgencyLevel), default=UrgencyLevel.LOW)
    
    # Location data
    pickup_address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    availability_window: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Status
    is_claimed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
