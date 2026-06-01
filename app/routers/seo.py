"""SEO techniczne: robots.txt i sitemap.xml (generowane dynamicznie z bazy).

Oba pliki są w korzeniu (bez prefiksu języka):
    /robots.txt
    /sitemap.xml

Sitemap zawiera wszystkie strony w obu językach z adnotacjami hreflang
(xhtml:link), co wzmacnia sygnał wielojęzyczności dla wyszukiwarek.
"""

from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.i18n import DEFAULT_LANG, HREFLANG, LANGUAGES
from app.models import (
    Author,
    BettingCategory,
    BlogPost,
    Bookmaker,
    Casino,
    Category,
    Slot,
)
from app.models.bonus import BONUS_TYPE_SLUGS
from app.payments import PAYMENT_METHODS

router = APIRouter()


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> str:
    base = settings.site_url.rstrip("/")
    return "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {base}/sitemap.xml",
            "",
        ]
    )


@router.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)) -> Response:
    base = settings.site_url.rstrip("/")
    groups = _collect_url_groups(db)
    return Response(content=_render_sitemap(base, groups), media_type="application/xml")


def _collect_url_groups(db: Session) -> list[dict[str, str]]:
    """Zwraca listę grup URL-i. Każda grupa to {lang: ścieżka} dla tej samej strony."""
    groups: list[dict[str, str]] = []

    def add_all_langs(path_template: str) -> None:
        groups.append({lang: path_template.format(lang=lang) for lang in LANGUAGES})

    # Strona główna
    add_all_langs("/{lang}/")
    # Strony statyczne
    for page in ("18plus", "pro-nas", "privacy"):
        add_all_langs(f"/{{lang}}/{page}/")
    # Bonusy: indeks + typy
    add_all_langs("/{lang}/bonusy/")
    for slug in BONUS_TYPE_SLUGS:
        add_all_langs(f"/{{lang}}/bonusy/{slug}/")
    # Blog: indeks
    add_all_langs("/{lang}/blog/")
    # Metody płatności
    for slug in PAYMENT_METHODS:
        add_all_langs(f"/{{lang}}/oplata/{slug}/")
    # Bukmacherzy: indeks + kategorie zakładów
    add_all_langs("/{lang}/bukmekery/")
    for slug in db.scalars(select(BettingCategory.slug)):
        add_all_langs(f"/{{lang}}/bukmekery/{slug}/")
    # Sloty: indeks + darmowe
    add_all_langs("/{lang}/igrovi-avtomaty/")
    add_all_langs("/{lang}/igrovi-avtomaty/bezkoshtovno/")

    # Kasyna (opublikowane)
    for slug in db.scalars(
        select(Casino.slug).where(Casino.is_published.is_(True))
    ):
        groups.append({lang: f"/{lang}/casino/{slug}/" for lang in LANGUAGES})

    # Kategorie kasyn
    for slug in db.scalars(select(Category.slug)):
        groups.append({lang: f"/{lang}/kategoriya/{slug}/" for lang in LANGUAGES})

    # Bukmacherzy (opublikowani)
    for slug in db.scalars(
        select(Bookmaker.slug).where(Bookmaker.is_published.is_(True))
    ):
        groups.append({lang: f"/{lang}/bukmeker/{slug}/" for lang in LANGUAGES})

    # Sloty (opublikowane)
    for slug in db.scalars(select(Slot.slug).where(Slot.is_published.is_(True))):
        groups.append({lang: f"/{lang}/slot/{slug}/" for lang in LANGUAGES})

    # Wpisy bloga — tylko języki, w których wpis istnieje
    for post in db.scalars(
        select(BlogPost).where(BlogPost.is_published.is_(True))
    ):
        langs = {
            lang: f"/{lang}/blog/{post.slug}/"
            for lang in LANGUAGES
            if getattr(post, f"title_{lang}")
        }
        if langs:
            groups.append(langs)

    # Autorzy — tylko języki, w których autor ma imię
    for author in db.scalars(select(Author)):
        langs = {
            lang: f"/{lang}/avtor/{author.slug}/"
            for lang in LANGUAGES
            if getattr(author, f"name_{lang}")
        }
        if langs:
            groups.append(langs)

    return groups


def _render_sitemap(base: str, groups: list[dict[str, str]]) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    for langs in groups:
        alternates = [
            (HREFLANG.get(lang, lang), base + path) for lang, path in langs.items()
        ]
        xdefault = base + (langs.get(DEFAULT_LANG) or next(iter(langs.values())))

        for path in langs.values():
            parts.append("  <url>")
            parts.append(f"    <loc>{escape(base + path)}</loc>")
            for hreflang, href in alternates:
                parts.append(
                    f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{escape(href)}"/>'
                )
            parts.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{escape(xdefault)}"/>'
            )
            parts.append("  </url>")

    parts.append("</urlset>")
    return "\n".join(parts)
