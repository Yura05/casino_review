"""Router metod płatności: /{lang}/oplata/{slug}/ — poradnik + kasyna z metodą."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import Casino
from app.payments import get_method
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/oplata/{slug}/")
def payment_page(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    method = get_method(slug, lang)
    if method is None:
        raise HTTPException(status_code=404, detail="Unknown payment method")

    # Kasyna, które mają którykolwiek z tokenów metody w polu payment_methods (CSV)
    conditions = [Casino.payment_methods.ilike(f"%{token}%") for token in method["tokens"]]
    casinos = db.scalars(
        select(Casino)
        .where(Casino.is_published.is_(True), or_(*conditions))
        .order_by(Casino.rating.desc())
        .options(
            selectinload(Casino.bonuses),
            selectinload(Casino.categories),
        )
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="payment.html",
        context=page_context(
            request, lang, method=method, casinos=casinos, author=get_default_author(db)
        ),
    )
