"""Router stron kategorii kasyn: /{lang}/kategoriya/{slug}/ — kasyna w danej kategorii."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import Casino, Category
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/kategoriya/{slug}/")
def category_page(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    category = db.scalars(select(Category).where(Category.slug == slug)).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    casinos = db.scalars(
        select(Casino)
        .where(
            Casino.is_published.is_(True),
            Casino.categories.any(Category.slug == slug),
        )
        .order_by(Casino.rating.desc())
        .options(
            selectinload(Casino.bonuses),
            selectinload(Casino.categories),
        )
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context=page_context(
            request, lang, category=category, casinos=casinos, author=get_default_author(db)
        ),
    )
