"""Router strony głównej: lista opublikowanych kasyn wg ratingu."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import page_context, validate_lang
from app.models import Casino
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/")
def home(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    casinos = db.scalars(
        select(Casino)
        .where(Casino.is_published.is_(True))
        .order_by(Casino.rating.desc())
        .options(
            selectinload(Casino.bonuses),
            selectinload(Casino.categories),
        )
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(request, lang, casinos=casinos),
    )
