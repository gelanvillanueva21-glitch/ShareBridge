import enum
from datetime import datetime
from sqlalchemy import String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class PhotoPurpose(str, enum.Enum):
    PROFILE = "profile"                 # Donator/Volunteer profile picture
    DONATION_POST = "donation_post"     # Picture of the goods being donated (Public)
    DELIVERY_PROOF = "delivery_proof"   # Social media post of successful handoff (Public)
    PRIVATE_MESSAGE = "private_message" # Private proof sent in PM (Private)
    ID_VERIFICATION = "id_verification" # Volunteer ID proof for admins (Strictly Private)

class Photo(Base):
    """
    Centralized table for all media/images uploaded to ShareBridge.
    Tracks who uploaded it, where the file lives, and what it's used for.
    """
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Path where the file is stored (e.g., app/data/donator/123.jpg)
    file_path: Mapped[str] = mapped_column(String, nullable=False) 
    
    # Context of the photo
    purpose: Mapped[PhotoPurpose] = mapped_column(Enum(PhotoPurpose), nullable=False)
    
    # Links to the specific feature (Donation.id, Message.id, Claim.id)
    # If purpose == PROFILE or ID_VERIFICATION, this can be left null or point to the User.id
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True) 
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

