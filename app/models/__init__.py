"""Pakiet modeli ORM.

Importujemy tu wszystkie modele, aby `Base.metadata` je "widziało"
(potrzebne np. przy tworzeniu tabel przez Base.metadata.create_all).
"""

from app.database import Base
from app.models.associations import bookmaker_betting_category, casino_category
from app.models.author import Author
from app.models.betting_category import BettingCategory
from app.models.blog import BlogPost
from app.models.bonus import Bonus
from app.models.bookmaker import Bookmaker
from app.models.casino import Casino
from app.models.casino_faq import CasinoFaq
from app.models.category import Category
from app.models.slot import Slot

__all__ = [
    "Base",
    "Casino",
    "CasinoFaq",
    "Bonus",
    "Category",
    "BlogPost",
    "Author",
    "Bookmaker",
    "BettingCategory",
    "Slot",
    "casino_category",
    "bookmaker_betting_category",
]
