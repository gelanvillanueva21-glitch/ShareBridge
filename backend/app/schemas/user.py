from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    role: UserRole = UserRole.DONOR


class UserCreate(UserBase):
    """Schema for user registration. Includes the raw password (will be hashed)."""
    password: str


class UserRead(UserBase):
    """
    Schema for returning user data to the frontend.
    Notice: 'password' and 'hashed_password' are NOT here — they are never sent back.
    """
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Auth Token Schemas
# ---------------------------------------------------------------------------

class TokenResponse(BaseModel):
    """
    What the /auth/login endpoint returns.
    Only the short-lived access token is in the JSON body.
    The refresh token is set as an HttpOnly cookie by the server automatically.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class LoginRequest(BaseModel):
    """What the /auth/login endpoint expects from the frontend."""
    email: EmailStr
    password: str
