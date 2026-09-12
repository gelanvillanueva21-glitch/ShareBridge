import enum
from datetime import datetime
from sqlalchemy import String, Enum, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class UserRole(str, enum.Enum):
    DONOR = "donor"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"
    # Phase 2: COMMUNITY = "community" (for anonymous receivers)

class User(Base):
    """
    User model handles authentication and profiles.
    Depending on the 'role', different fields might apply.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    # Public display name ("Volunteer #12" if privacy is strict)
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.DONOR)
    
    # VOLUNTEER SPECIFIC
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
