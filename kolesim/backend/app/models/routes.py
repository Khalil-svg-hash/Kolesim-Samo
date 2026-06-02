from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from app.core.database import Base


class Route(Base):
    __tablename__ = "routes"
    __table_args__ = (
        CheckConstraint("duration_days BETWEEN 1 AND 2", name="ck_routes_duration_days"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    duration_days: Mapped[int] = mapped_column(SmallInteger, server_default=text("1"))
    distance_km: Mapped[float | None] = mapped_column(Numeric(6, 2))
    difficulty: Mapped[str | None] = mapped_column(String(50))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    is_editorial: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    is_published: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    is_free: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    view_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    created_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
