from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MediaResponse(BaseModel):
    id: UUID
    entity_type: str
    entity_id: UUID
    url: str
    thumbnail_url: str | None = None
    caption: str | None = None
    media_type: str
    sort_order: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
