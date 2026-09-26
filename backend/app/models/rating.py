# // app/models/rating.py
"""Rating models for donors and volunteers.
Separate tables make it easy to query ratings per role and keep the aggregate
logic simple. Each rating stores who gave it (rater_id), who received it
(rated_id), a numeric score and an optional comment.
"""

from datetime import datetime
from sqlalchemy import Float, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class DonorRating(Base):
    __tablename__ = "donor_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Volunteer who gives the rating
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Donor who receives the rating
    rated_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class VolunteerRating(Base):
    __tablename__ = "volunteer_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Donor who gives the rating
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Volunteer who receives the rating
    rated_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
