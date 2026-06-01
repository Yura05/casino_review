"""Router bukmacherów:
    /{lang}/bukmekery/           — wszystkie recenzje bukmacherów
    /{lang}/bukmekery/{slug}/    — bukmacherzy wg kategorii zakładów
    /{lang}/bukmeker/{slug}/     — szczegółowa recenzja bukmachera
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import BettingCategory, Bookmaker
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/bukmekery/")
def bookmaker_index(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    bookmakers = db.scalars(
        select(Bookmaker)
        .where(Bookmaker.is_published.is_(True))
        .order_by(Bookmaker.rating.desc())
        .options(selectinload(Bookmaker.betting_categories))
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="bookmaker_list.html",
        context=page_context(
            request, lang, bookmakers=bookmakers, category=None, author=get_default_author(db)
        ),
    )


@router.get("/{lang}/bukmekery/{slug}/")
def bookmaker_category(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    category = db.scalars(
        select(BettingCategory).where(BettingCategory.slug == slug)
    ).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Betting category not found")

    bookmakers = db.scalars(
        select(Bookmaker)
        .where(
            Bookmaker.is_published.is_(True),
            Bookmaker.betting_categories.any(BettingCategory.slug == slug),
        )
        .order_by(Bookmaker.rating.desc())
        .options(selectinload(Bookmaker.betting_categories))
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="bookmaker_list.html",
        context=page_context(
            request, lang, bookmakers=bookmakers, category=category, author=get_default_author(db)
        ),
    )


@router.get("/{lang}/bukmeker/{slug}/")
def bookmaker_detail(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    bookmaker = db.scalars(
        select(Bookmaker)
        .where(Bookmaker.slug == slug, Bookmaker.is_published.is_(True))
        .options(selectinload(Bookmaker.betting_categories))
    ).first()
    if bookmaker is None:
        raise HTTPException(status_code=404, detail="Bookmaker not found")

    schema = {
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {"@type": "Organization", "name": bookmaker.name},
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": str(bookmaker.rating),
            "bestRating": "5",
        },
        "author": {"@type": "Organization", "name": settings.site_name},
    }

    return templates.TemplateResponse(
        request=request,
        name="bookmaker_detail.html",
        context=page_context(
            request,
            lang,
            bookmaker=bookmaker,
            schema=schema,
            current_year=datetime.now().year,
            author=get_default_author(db),
        ),
    )
