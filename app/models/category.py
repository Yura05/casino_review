"""Model kategorii/tagu — do filtrowania kasyn i stron SEO."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import casino_category
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.casino import Casino


class Category(LocalizedMixin, Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    # Treść dwujęzyczna
    name_uk: Mapped[str] = mapped_column(String(120))
    name_ru: Mapped[str] = mapped_column(String(120))

    casinos: Mapped[list[Casino]] = relationship(
        secondary=casino_category, back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<Category {self.slug!r}>"
