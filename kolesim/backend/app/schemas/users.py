from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    wheelchair_type: str | None = None
    min_door_width_cm: int = Field(default=60, ge=30, le=200)
    needs_accessible_wc: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    wheelchair_type: str | None = None
    min_door_width_cm: int | None = Field(default=None, ge=30, le=200)
    needs_accessible_wc: bool | None = None


class UserResponse(UserBase):
    id: UUID
    avatar_url: str | None = None
    is_active: bool
    is_verified: bool
    is_admin: bool
    subscription_status: str
    subscription_expires_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
