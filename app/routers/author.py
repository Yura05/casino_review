"""Router strony autora: /{lang}/avtor/{slug}/ (E-E-A-T)."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import page_context, validate_lang
from app.models import Author
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/avtor/{slug}/")
def author_page(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    author = db.scalars(select(Author).where(Author.slug == slug)).first()
    if author is None or author.loc("name", lang) is None:
        raise HTTPException(status_code=404, detail="Author not found")

    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": author.loc("name", lang),
        "jobTitle": author.loc("role", lang),
        "description": author.loc("bio", lang),
        "url": f"{settings.site_url.rstrip('/')}/{lang}/avtor/{author.slug}/",
    }

    return templates.TemplateResponse(
        request=request,
        name="author.html",
        context=page_context(request, lang, author=author, schema=schema),
    )
