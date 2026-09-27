# backend/app/schemas/profile.py
"""Pydantic schemas for the Profile model.
These are used by the FastAPI routers to validate request bodies and shape responses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProfileBase(BaseModel):
    """Common fields for create and update operations."""
    display_name: Optional[str] = Field(None, description="Public display name shown on the profile")
    bio: Optional[str] = Field(None, description="Short biography or description")
    city: Optional[str] = Field(None, description="City of residence")
    goal: Optional[float] = Field(None, description="Personal ratings goal (e.g., donation target)")


class ProfileCreate(ProfileBase):
    """Schema for creating a profile – all fields are optional because a profile can be created lazily.
    The router will associate it with the currently authenticated user.
    """
    pass


class ProfileUpdate(ProfileBase):
    """Schema for partial updates – FastAPI will treat missing fields as "no change".
    """
    pass


class ProfileRead(ProfileBase):
    """Schema returned to the client.
    Includes identifiers and the URL of the profile picture if one exists.
    """
    id: int = Field(..., description="Profile primary key")
    user_id: int = Field(..., description="FK to the owning user")
    profile_photo_url: Optional[str] = Field(None, description="URL of the profile picture (if set)")

    model_config = ConfigDict(from_attributes=True)


class ProfileSearchResult(ProfileRead):
    """Lightweight profile payload used for search results in the public API."""
    pass
