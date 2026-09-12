from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class Message(Base):
    """
    Represents a direct message (PM) between a Donor and a Volunteer.
    Supports text and optional image attachments (like proofs).
    """
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Optional context (which donation they are talking about)
    donation_id: Mapped[int | None] = mapped_column(ForeignKey("donations.id"), nullable=True)
    
    content: Mapped[str | None] = mapped_column(String, nullable=True) # The text message
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

