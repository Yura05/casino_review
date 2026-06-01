"""Model automatu do gry (slot)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import LocalizedMixin


class Slot(LocalizedMixin, Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    image: Mapped[str | None] = mapped_column(String(255), default=None)

    # Pola neutralne językowo
    provider: Mapped[str | None] = mapped_column(String(120), default=None)
    rtp: Mapped[str | None] = mapped_column(String(20), default=None)   # np. "96.21%"
    paylines: Mapped[str | None] = mapped_column(String(40), default=None)  # np. "10" / "243"

    # Treść dwujęzyczna
    name_uk: Mapped[str] = mapped_column(String(120))
    name_ru: Mapped[str] = mapped_column(String(120))
    volatility_uk: Mapped[str | None] = mapped_column(String(40), default=None)
    volatility_ru: Mapped[str | None] = mapped_column(String(40), default=None)
    description_uk: Mapped[str | None] = mapped_column(Text, default=None)
    description_ru: Mapped[str | None] = mapped_column(Text, default=None)

    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Slot {self.slug!r}>"
