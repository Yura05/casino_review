"""Model bonusu — przypisany do kasyna (jedno kasyno ma wiele bonusów)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.casino import Casino

# Dozwolone typy bonusów (jako string; walidację robimy w kodzie/seedzie)
BONUS_TYPES = (
    "no_deposit",
    "registration",
    "first_deposit",
    "free_spins",
    "birthday",
    "match",
)

# Mapowanie: slug w URL -> wewnętrzny typ bonusu.
# Kolejność = kolejność wyświetlania w menu i na stronie /bonusy/.
BONUS_TYPE_SLUGS: dict[str, str] = {
    "no-deposit": "no_deposit",
    "registration": "registration",
    "first-deposit": "first_deposit",
    "free-spins": "free_spins",
    "birthday": "birthday",
    "match": "match",
}


class Bonus(LocalizedMixin, Base):
    __tablename__ = "bonus"

    id: Mapped[int] = mapped_column(primary_key=True)
    casino_id: Mapped[int] = mapped_column(
        ForeignKey("casino.id", ondelete="CASCADE"), index=True
    )

    type: Mapped[str] = mapped_column(String(30))  # no_deposit | free_spins | match
    amount: Mapped[str | None] = mapped_column(String(120), default=None)  # np. "100% do 500€" / "50 FS"

    # Warunki bonusu (do porownan i tabeli) — krotkie etykiety, np. "x35", "100 ₴"
    wager: Mapped[str | None] = mapped_column(String(50), default=None)  # np. "x35", "x40", "—"
    min_deposit: Mapped[str | None] = mapped_column(String(50), default=None)  # np. "100 ₴", "—"

    # Treść dwujęzyczna
    terms_uk: Mapped[str | None] = mapped_column(Text, default=None)
    terms_ru: Mapped[str | None] = mapped_column(Text, default=None)

    casino: Mapped[Casino] = relationship(back_populates="bonuses")

    def __repr__(self) -> str:
        return f"<Bonus {self.type!r} casino_id={self.casino_id}>"
