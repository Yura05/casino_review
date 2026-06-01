"""Tabele łączące (many-to-many)."""

from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

# Kasyno <-> Kategoria (relacja wiele-do-wielu, służy do filtrowania i stron SEO)
casino_category = Table(
    "casino_category",
    Base.metadata,
    Column("casino_id", ForeignKey("casino.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("category.id", ondelete="CASCADE"), primary_key=True),
)

# Bukmacher <-> Kategoria zakładów (np. piłka nożna, e-sport, boks)
bookmaker_betting_category = Table(
    "bookmaker_betting_category",
    Base.metadata,
    Column("bookmaker_id", ForeignKey("bookmaker.id", ondelete="CASCADE"), primary_key=True),
    Column("betting_category_id", ForeignKey("betting_category.id", ondelete="CASCADE"), primary_key=True),
)
