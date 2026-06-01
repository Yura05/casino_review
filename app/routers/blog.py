"""Router bloga: lista artykułów (/blog/) i pojedynczy artykuł (/blog/{slug}/)."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import page_context, validate_lang
from app.models import BlogPost
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/blog/")
def blog_index(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    # Pokazujemy tylko wpisy, które mają tytuł w bieżącym języku
    title_col = getattr(BlogPost, f"title_{lang}")
    posts = db.scalars(
        select(BlogPost)
        .where(BlogPost.is_published.is_(True), title_col.is_not(None))
        .order_by(BlogPost.published_at.desc())
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="blog_index.html",
        context=page_context(request, lang, posts=posts),
    )


@router.get("/{lang}/blog/{slug}/")
def blog_post(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    post = db.scalars(
        select(BlogPost).where(
            BlogPost.slug == slug, BlogPost.is_published.is_(True)
        )
    ).first()

    # 404, jeśli wpisu nie ma lub nie istnieje w bieżącym języku
    if post is None or post.loc("title", lang) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    body = post.loc("body", lang) or ""
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.loc("title", lang),
        "datePublished": post.published_at.date().isoformat(),
        "author": {"@type": "Organization", "name": settings.site_name},
    }

    return templates.TemplateResponse(
        request=request,
        name="blog_post.html",
        context=page_context(request, lang, post=post, paragraphs=paragraphs, schema=schema),
    )
