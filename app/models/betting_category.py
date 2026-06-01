"""Model kategorii zakładów (typy sportu / rynki) — do menu "Bukmacherzy"."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import bookmaker_betting_category
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.bookmaker import Bookmaker


class BettingCategory(LocalizedMixin, Base):
    __tablename__ = "betting_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    name_uk: Mapped[str] = mapped_column(String(160))
    name_ru: Mapped[str] = mapped_column(String(160))

    bookmakers: Mapped[list[Bookmaker]] = relationship(
        secondary=bookmaker_betting_category, back_populates="betting_categories"
    )

    def __repr__(self) -> str:
        return f"<BettingCategory {self.slug!r}>"
