from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.media import MediaResponse


class AccessibilityBase(BaseModel):
    has_step_free_entrance: bool | None = None
    entrance_door_width_cm: int | None = None
    has_ramp: bool | None = None
    has_elevator: bool | None = None
    elevator_door_width_cm: int | None = None
    has_accessible_wc: bool | None = None
    wc_door_width_cm: int | None = None
    has_accessible_parking: bool | None = None
    parking_distance_m: int | None = None
    floor_surface: str | None = None
    extra_notes: str | None = None


class PlaceBase(BaseModel):
    name: str
    description: str | None = None
    category: Literal["hotel", "restaurant", "attraction", "transport", "service"]
    address: str
    city: str = "Москва"
    latitude: Decimal
    longitude: Decimal
    entrance_lat: Decimal | None = None
    entrance_lng: Decimal | None = None
    parking_lat: Decimal | None = None
    parking_lng: Decimal | None = None
    price_level: int | None = Field(default=None, ge=1, le=3)
    is_free_entry: bool = False
    working_hours: dict | None = None
    phone: str | None = None
    website_url: str | None = None


class PlaceCreate(PlaceBase):
    accessibility: AccessibilityBase | None = None
    is_free: bool = False


class PlaceUpdate(PlaceBase):
    accessibility: AccessibilityBase | None = None


class PlaceResponse(PlaceBase):
    id: UUID
    slug: str
    is_verified: bool
    verified_at: datetime | None = None
    is_free: bool
    is_published: bool
    media: list[MediaResponse] = []
    accessibility: AccessibilityBase | None = None
    avg_rating: float | None = None
    review_count: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlaceListResponse(BaseModel):
    items: list[PlaceResponse]
    total: int
    page: int
    limit: int
    pages: int
