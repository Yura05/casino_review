"""Model wpisu na blogu (artykuły, poradniki)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import LocalizedMixin


class BlogPost(LocalizedMixin, Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)

    # Treść dwujęzyczna
    title_uk: Mapped[str | None] = mapped_column(String(200), default=None)
    title_ru: Mapped[str | None] = mapped_column(String(200), default=None)
    body_uk: Mapped[str | None] = mapped_column(Text, default=None)
    body_ru: Mapped[str | None] = mapped_column(Text, default=None)
    meta_description_uk: Mapped[str | None] = mapped_column(String(300), default=None)
    meta_description_ru: Mapped[str | None] = mapped_column(String(300), default=None)

    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<BlogPost {self.slug!r}>"
