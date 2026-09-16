from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    role: UserRole = UserRole.DONOR

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
