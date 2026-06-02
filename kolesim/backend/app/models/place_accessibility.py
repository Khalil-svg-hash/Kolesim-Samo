from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from app.core.database import Base


class PlaceAccessibility(Base):
    __tablename__ = "place_accessibility"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    place_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("places.id", ondelete="CASCADE"), unique=True
    )
    has_step_free_entrance: Mapped[bool | None] = mapped_column(Boolean)
    entrance_door_width_cm: Mapped[int | None] = mapped_column(Integer)
    has_ramp: Mapped[bool | None] = mapped_column(Boolean)
    ramp_angle_deg: Mapped[float | None] = mapped_column(Numeric(4, 1))
    has_elevator: Mapped[bool | None] = mapped_column(Boolean)
    elevator_door_width_cm: Mapped[int | None] = mapped_column(Integer)
    elevator_notes: Mapped[str | None] = mapped_column(Text)
    has_accessible_wc: Mapped[bool | None] = mapped_column(Boolean)
    wc_door_width_cm: Mapped[int | None] = mapped_column(Integer)
    wc_notes: Mapped[str | None] = mapped_column(Text)
    has_accessible_parking: Mapped[bool | None] = mapped_column(Boolean)
    parking_distance_m: Mapped[int | None] = mapped_column(Integer)
    floor_surface: Mapped[str | None] = mapped_column(String(100))
    extra_notes: Mapped[str | None] = mapped_column(Text)
    last_checked_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    checked_by: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
