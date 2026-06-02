from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(Text)
    wheelchair_type: Mapped[str | None] = mapped_column(String(50))
    min_door_width_cm: Mapped[int] = mapped_column(Integer, server_default=text("60"))
    needs_accessible_wc: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    subscription_status: Mapped[str] = mapped_column(
        String(50), server_default=text("'free'")
    )
    subscription_expires_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
