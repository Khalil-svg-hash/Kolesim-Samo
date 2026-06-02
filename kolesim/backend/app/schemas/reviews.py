from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.media import MediaResponse


class ReviewCreate(BaseModel):
    entity_type: Literal["place", "route"]
    entity_id: UUID
    rating: int = Field(ge=1, le=5)
    accessibility_rating: int = Field(ge=1, le=5)
    text: str | None = None
    visited_at: date | None = None
    wheelchair_type: str | None = None


class ReviewModerate(BaseModel):
    status: Literal["approved", "rejected"]
    note: str | None = None


class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    entity_type: str
    entity_id: UUID
    rating: int
    accessibility_rating: int
    text: str | None = None
    visited_at: date | None = None
    wheelchair_type: str | None = None
    moderation_status: str
    moderation_note: str | None = None
    moderated_by: UUID | None = None
    moderated_at: datetime | None = None
    created_at: datetime
    media: list[MediaResponse] = []

    model_config = ConfigDict(from_attributes=True)
