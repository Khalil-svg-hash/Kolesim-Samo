from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from app.core.database import Base


class RoutePlace(Base):
    __tablename__ = "route_places"
    __table_args__ = (
        UniqueConstraint("route_id", "order_index", name="uq_route_places_order"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    route_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE")
    )
    place_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"))
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    day_number: Mapped[int] = mapped_column(SmallInteger, server_default=text("1"))
    notes: Mapped[str | None] = mapped_column(Text)
    estimated_duration_min: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
