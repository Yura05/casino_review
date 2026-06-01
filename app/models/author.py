"""Model autora/redaktora (E-E-A-T: autorytet i zaufanie dla treści)."""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import LocalizedMixin


class Author(LocalizedMixin, Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    avatar: Mapped[str | None] = mapped_column(String(255), default=None)  # ścieżka względem /static

    # Treść dwujęzyczna
    name_uk: Mapped[str] = mapped_column(String(120))
    name_ru: Mapped[str] = mapped_column(String(120))
    role_uk: Mapped[str | None] = mapped_column(String(200), default=None)
    role_ru: Mapped[str | None] = mapped_column(String(200), default=None)
    bio_uk: Mapped[str | None] = mapped_column(Text, default=None)
    bio_ru: Mapped[str | None] = mapped_column(Text, default=None)

    def __repr__(self) -> str:
        return f"<Author {self.slug!r}>"
