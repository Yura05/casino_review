"""Model kasyna.

Treść dwujęzyczna trzymana w osobnych kolumnach na język (_uk / _ru).
Pola "neutralne językowo" (rating, licencja, link afiliacyjny) bez sufiksu.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import casino_category
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.bonus import Bonus
    from app.models.casino_faq import CasinoFaq
    from app.models.category import Category


class Casino(LocalizedMixin, Base):
    __tablename__ = "casino"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    logo: Mapped[str | None] = mapped_column(String(255), default=None)  # ścieżka względem /static, np. "img/casinos/spincity.svg"

    # Pola neutralne językowo
    license: Mapped[str | None] = mapped_column(String(120), default=None)
    license_number: Mapped[str | None] = mapped_column(String(120), default=None)
    payment_methods: Mapped[str | None] = mapped_column(String(255), default=None)  # CSV, np. "Visa,Mastercard,BTC"
    affiliate_link: Mapped[str | None] = mapped_column(String(500), default=None)
    established: Mapped[int | None] = mapped_column(Integer, default=None)  # rok założenia
    min_deposit: Mapped[str | None] = mapped_column(String(50), default=None)  # np. "20 €"
    badges: Mapped[str | None] = mapped_column(String(120), default=None)  # CSV kluczy bejdzy, np. "top,fast"

    # Oceny cząstkowe (0–5) — rozbicie ratingu na kryteria
    score_bonuses: Mapped[float | None] = mapped_column(Float, default=None)
    score_games: Mapped[float | None] = mapped_column(Float, default=None)
    score_payments: Mapped[float | None] = mapped_column(Float, default=None)
    score_support: Mapped[float | None] = mapped_column(Float, default=None)

    # Treść dwujęzyczna
    bonus_uk: Mapped[str | None] = mapped_column(String(255), default=None)
    bonus_ru: Mapped[str | None] = mapped_column(String(255), default=None)
    description_uk: Mapped[str | None] = mapped_column(Text, default=None)
    description_ru: Mapped[str | None] = mapped_column(Text, default=None)
    # Sekcje pełnej recenzji (Text; listy rozdzielane nową linią)
    pros_uk: Mapped[str | None] = mapped_column(Text, default=None)
    pros_ru: Mapped[str | None] = mapped_column(Text, default=None)
    cons_uk: Mapped[str | None] = mapped_column(Text, default=None)
    cons_ru: Mapped[str | None] = mapped_column(Text, default=None)
    overview_uk: Mapped[str | None] = mapped_column(Text, default=None)
    overview_ru: Mapped[str | None] = mapped_column(Text, default=None)
    games_uk: Mapped[str | None] = mapped_column(Text, default=None)
    games_ru: Mapped[str | None] = mapped_column(Text, default=None)
    payments_info_uk: Mapped[str | None] = mapped_column(Text, default=None)
    payments_info_ru: Mapped[str | None] = mapped_column(Text, default=None)
    security_uk: Mapped[str | None] = mapped_column(Text, default=None)
    security_ru: Mapped[str | None] = mapped_column(Text, default=None)
    support_uk: Mapped[str | None] = mapped_column(Text, default=None)
    support_ru: Mapped[str | None] = mapped_column(Text, default=None)
    withdrawal_time_uk: Mapped[str | None] = mapped_column(String(80), default=None)
    withdrawal_time_ru: Mapped[str | None] = mapped_column(String(80), default=None)
    verdict_uk: Mapped[str | None] = mapped_column(Text, default=None)
    verdict_ru: Mapped[str | None] = mapped_column(Text, default=None)

    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relacje
    bonuses: Mapped[list[Bonus]] = relationship(
        back_populates="casino", cascade="all, delete-orphan"
    )
    categories: Mapped[list[Category]] = relationship(
        secondary=casino_category, back_populates="casinos"
    )
    faqs: Mapped[list[CasinoFaq]] = relationship(
        back_populates="casino",
        cascade="all, delete-orphan",
        order_by="CasinoFaq.position",
    )

    def __repr__(self) -> str:
        return f"<Casino {self.slug!r} rating={self.rating}>"
