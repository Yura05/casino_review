"""Model bukmachera (zakłady sportowe) — analogiczny do kasyna."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import bookmaker_betting_category
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.betting_category import BettingCategory


class Bookmaker(LocalizedMixin, Base):
    __tablename__ = "bookmaker"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    logo: Mapped[str | None] = mapped_column(String(255), default=None)

    # Pola neutralne językowo
    license: Mapped[str | None] = mapped_column(String(120), default=None)
    license_number: Mapped[str | None] = mapped_column(String(120), default=None)
    payment_methods: Mapped[str | None] = mapped_column(String(255), default=None)
    affiliate_link: Mapped[str | None] = mapped_column(String(500), default=None)
    established: Mapped[int | None] = mapped_column(Integer, default=None)
    min_deposit: Mapped[str | None] = mapped_column(String(50), default=None)

    # Treść dwujęzyczna
    bonus_uk: Mapped[str | None] = mapped_column(String(255), default=None)
    bonus_ru: Mapped[str | None] = mapped_column(String(255), default=None)
    description_uk: Mapped[str | None] = mapped_column(Text, default=None)
    description_ru: Mapped[str | None] = mapped_column(Text, default=None)
    pros_uk: Mapped[str | None] = mapped_column(Text, default=None)
    pros_ru: Mapped[str | None] = mapped_column(Text, default=None)
    cons_uk: Mapped[str | None] = mapped_column(Text, default=None)
    cons_ru: Mapped[str | None] = mapped_column(Text, default=None)
    overview_uk: Mapped[str | None] = mapped_column(Text, default=None)
    overview_ru: Mapped[str | None] = mapped_column(Text, default=None)
    verdict_uk: Mapped[str | None] = mapped_column(Text, default=None)
    verdict_ru: Mapped[str | None] = mapped_column(Text, default=None)

    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    betting_categories: Mapped[list[BettingCategory]] = relationship(
        secondary=bookmaker_betting_category, back_populates="bookmakers"
    )

    def __repr__(self) -> str:
        return f"<Bookmaker {self.slug!r} rating={self.rating}>"
