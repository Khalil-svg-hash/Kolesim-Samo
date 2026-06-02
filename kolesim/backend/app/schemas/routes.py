from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.places import PlaceResponse


class RouteBase(BaseModel):
    title: str
    description: str | None = None
    duration_days: int = Field(default=1, ge=1, le=2)
    distance_km: float | None = None
    difficulty: Literal["easy", "medium", "hard"] | None = None
    tags: list[str] | None = None


class RouteCreate(RouteBase):
    is_free: bool = False


class RouteUpdate(RouteBase):
    is_free: bool | None = None
    is_published: bool | None = None


class RouteResponse(RouteBase):
    id: UUID
    slug: str
    is_editorial: bool
    is_published: bool
    is_free: bool
    view_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RouteConstructResponse(BaseModel):
    route: RouteResponse | None
    places: list[PlaceResponse]
    estimated_distance_km: float | None = None


class RouteListResponse(BaseModel):
    items: list[RouteResponse]
    total: int
    page: int
    limit: int
    pages: int
