"""Model FAQ kasyna (pytania i odpowiedzi w recenzji)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import LocalizedMixin

if TYPE_CHECKING:
    from app.models.casino import Casino


class CasinoFaq(LocalizedMixin, Base):
    __tablename__ = "casino_faq"

    id: Mapped[int] = mapped_column(primary_key=True)
    casino_id: Mapped[int] = mapped_column(
        ForeignKey("casino.id", ondelete="CASCADE"), index=True
    )
    position: Mapped[int] = mapped_column(Integer, default=0)

    question_uk: Mapped[str | None] = mapped_column(String(300), default=None)
    question_ru: Mapped[str | None] = mapped_column(String(300), default=None)
    answer_uk: Mapped[str | None] = mapped_column(Text, default=None)
    answer_ru: Mapped[str | None] = mapped_column(Text, default=None)

    casino: Mapped[Casino] = relationship(back_populates="faqs")
