"""Współdzielone zależności (dependencies) i pomocniki dla endpointów.

`validate_lang` — sprawdza, czy język z URL jest obsługiwany (inaczej 404).
`page_context`  — buduje wspólny kontekst dla szablonów (język, tłumaczenia,
                  URL-e alternatywnych języków, dane serwisu).
"""

from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.i18n import (
    DEFAULT_LANG,
    HREFLANG,
    LANG_LABELS,
    LANGUAGES,
    OG_LOCALE,
    alternate_urls,
    get_translations,
    is_supported,
)
from app.models import Author, BettingCategory, Category, Slot
from app.models.bonus import BONUS_TYPE_SLUGS
from app.payments import nav_items as payment_nav_items


def _db_nav(
    lang: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Kategorie kasyn, kategorie zakładów i sloty do menu (jeden zapyt do bazy)."""
    with SessionLocal() as db:
        cats = db.scalars(select(Category).order_by(Category.id)).all()
        bkcats = db.scalars(select(BettingCategory).order_by(BettingCategory.id)).all()
        slots = db.scalars(
            select(Slot).where(Slot.is_published.is_(True)).order_by(Slot.id)
        ).all()
        category_nav = [{"slug": c.slug, "name": c.loc("name", lang)} for c in cats]
        betting_nav = [{"slug": c.slug, "name": c.loc("name", lang)} for c in bkcats]
        slot_nav = [{"slug": s.slug, "name": s.loc("name", lang)} for s in slots]
        return category_nav, betting_nav, slot_nav


def validate_lang(lang: str) -> str:
    if not is_supported(lang):
        raise HTTPException(status_code=404, detail="Language not supported")
    return lang


def get_default_author(db: Session) -> Author | None:
    """Domyślny autor/redaktor serwisu (na razie jeden) — do bloku autora."""
    return db.scalars(select(Author).order_by(Author.id)).first()


def page_context(request: Request, lang: str, **extra) -> dict:
    translations = get_translations(lang)
    category_nav, betting_category_nav, slot_nav = _db_nav(lang)
    context = {
        "lang": lang,
        "t": translations,
        "languages": LANGUAGES,
        "default_lang": DEFAULT_LANG,
        "lang_labels": LANG_LABELS,
        "hreflang": HREFLANG,
        "og_locale": OG_LOCALE.get(lang, lang),
        "alt_urls": alternate_urls(request.url.path),
        "site_name": settings.site_name,
        "site_url": settings.site_url.rstrip("/"),
        "payment_methods": payment_nav_items(lang),
        "bonus_nav": [
            {"slug": slug, "name": translations.get(f"bonus_{btype}", btype)}
            for slug, btype in BONUS_TYPE_SLUGS.items()
        ],
        "category_nav": category_nav,
        "betting_category_nav": betting_category_nav,
        "slot_nav": slot_nav,
    }
    context.update(extra)
    return context
