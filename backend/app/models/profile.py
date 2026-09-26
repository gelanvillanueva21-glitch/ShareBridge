# // app/models/profile.py
"""User profile information separated from the core User model.
This model holds personal details that a user can edit: full name, bio, city, a personal goal, and a profile picture.
It has a one‑to‑one relationship with `User` (user_id is unique) and an optional FK to a `Photo` where purpose = PROFILE.
"""

import enum
from datetime import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    bio: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    goal: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Optional link to a profile picture stored in the Photo table.
    profile_photo_id: Mapped[int | None] = mapped_column(ForeignKey("photos.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Relationships – optional, useful for ORM navigation.
    user = relationship("User", back_populates="profile", uselist=False)
    profile_photo = relationship("Photo", foreign_keys=[profile_photo_id])
