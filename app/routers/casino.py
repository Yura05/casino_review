"""Router szczegółowej recenzji kasyna: /{lang}/casino/{slug}/."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.competitors import competitors_for
from app.config import settings
from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import Casino
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/casino/{slug}/")
def casino_detail(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    casino = db.scalars(
        select(Casino)
        .where(Casino.slug == slug, Casino.is_published.is_(True))
        .options(
            selectinload(Casino.bonuses),
            selectinload(Casino.categories),
            selectinload(Casino.faqs),
        )
    ).first()

    if casino is None:
        raise HTTPException(status_code=404, detail="Casino not found")

    # Schema.org (JSON-LD) — Review z reviewRating (kwalifikuje się do
    # "review snippet" w Google: gwiazdki w wynikach wyszukiwania).
    site = settings.site_url.rstrip("/")
    review_url = f"{site}/{lang}/casino/{casino.slug}/"

    item_reviewed: dict = {
        "@type": "Organization",
        "name": casino.name,
    }
    if casino.logo:
        item_reviewed["image"] = f"{site}/static/{casino.logo}"

    # Zagregowana ocena z ocen cząstkowych (kryteria redakcyjne) — jeśli są.
    # ratingCount = liczba ocenionych kryteriów (uczciwa podstawa agregatu).
    sub_scores = [
        s for s in (
            casino.score_bonuses,
            casino.score_games,
            casino.score_payments,
            casino.score_support,
        ) if s is not None
    ]
    if sub_scores:
        item_reviewed["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": f"{casino.rating:.1f}",
            "bestRating": "5",
            "worstRating": "1",
            "ratingCount": str(len(sub_scores)),
        }

    review_body = (
        casino.loc("verdict", lang)
        or casino.loc("description", lang)
        or casino.loc("overview", lang)
    )

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Review",
        "name": f"{casino.name} — {settings.site_name}",
        "url": review_url,
        "itemReviewed": item_reviewed,
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": f"{casino.rating:.1f}",
            "bestRating": "5",
            "worstRating": "1",
        },
        "author": {"@type": "Organization", "name": settings.site_name, "url": site},
        "publisher": {"@type": "Organization", "name": settings.site_name},
        "datePublished": casino.created_at.date().isoformat(),
    }
    if review_body:
        review_schema["reviewBody"] = review_body

    # Schema.org (JSON-LD) — FAQPage (rich results dla pytań i odpowiedzi)
    faq_entries = [
        {
            "@type": "Question",
            "name": f.loc("question", lang),
            "acceptedAnswer": {"@type": "Answer", "text": f.loc("answer", lang)},
        }
        for f in casino.faqs
        if f.loc("question", lang) and f.loc("answer", lang)
    ]
    schemas = [review_schema]
    if faq_entries:
        schemas.append(
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entries}
        )

    return templates.TemplateResponse(
        request=request,
        name="casino_detail.html",
        context=page_context(
            request,
            lang,
            casino=casino,
            schemas=schemas,
            current_year=datetime.now().year,
            competitors=competitors_for(casino.id, casino.slug),
            author=get_default_author(db),
        ),
    )
