import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class ClaimStatus(str, enum.Enum):
    PENDING = "pending"       # Volunteer claimed it, waiting for donor to confirm or just handoff
    CONFIRMED = "confirmed"   # Donor confirmed the volunteer can pick it up
    COMPLETED = "completed"   # Handoff is done
    CANCELLED = "cancelled"

class Claim(Base):
    """
    Represents a volunteer claiming a donation to pick it up.
    """
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    donation_id: Mapped[int] = mapped_column(ForeignKey("donations.id"), nullable=False)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    status: Mapped[ClaimStatus] = mapped_column(Enum(ClaimStatus), default=ClaimStatus.PENDING)
    
    # Social media proof of delivery
    delivery_caption: Mapped[str | None] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
