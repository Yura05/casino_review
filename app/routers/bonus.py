"""Router bonusów: lista typów (/bonusy/) i kasyna wg typu bonusu (/bonusy/{typ}/)."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import Bonus, Casino
from app.models.bonus import BONUS_TYPE_SLUGS
from app.templating import templates

router = APIRouter()


@router.get("/{lang}/bonusy/")
def bonus_index(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    bonus_types = [{"slug": slug, "type": btype} for slug, btype in BONUS_TYPE_SLUGS.items()]

    # TOP-10 bonusow — laczymy z kasynem, sortujemy po ocenie kasyna malejaco.
    top_bonuses = db.scalars(
        select(Bonus)
        .join(Bonus.casino)
        .where(Casino.is_published.is_(True))
        .order_by(Casino.rating.desc(), Bonus.id.asc())
        .options(selectinload(Bonus.casino))
        .limit(10)
    ).all()

    # Odwrotna mapa: wewnetrzny type -> slug w URL (do linkow w tabeli/karcie)
    type_to_slug = {v: k for k, v in BONUS_TYPE_SLUGS.items()}

    return templates.TemplateResponse(
        request=request,
        name="bonus_index.html",
        context=page_context(
            request, lang,
            bonus_types=bonus_types,
            top_bonuses=top_bonuses,
            type_to_slug=type_to_slug,
            author=get_default_author(db),
        ),
    )


@router.get("/{lang}/bonusy/{typ}/")
def bonus_list(
    typ: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    bonus_type = BONUS_TYPE_SLUGS.get(typ)
    if bonus_type is None:
        raise HTTPException(status_code=404, detail="Unknown bonus type")

    # Pobieramy konkretne bonusy danego typu (a nie kasyna) — kazda karta to bonus.
    bonuses = db.scalars(
        select(Bonus)
        .join(Bonus.casino)
        .where(
            Casino.is_published.is_(True),
            Bonus.type == bonus_type,
        )
        .order_by(Casino.rating.desc(), Bonus.id.asc())
        .options(selectinload(Bonus.casino))
    ).all()

    # Odwrotna mapa: wewnetrzny type -> slug w URL (dla linkow w karcie)
    type_to_slug = {v: k for k, v in BONUS_TYPE_SLUGS.items()}

    return templates.TemplateResponse(
        request=request,
        name="bonus_list.html",
        context=page_context(
            request, lang,
            bonuses=bonuses,
            typ=typ,
            bonus_type=bonus_type,
            type_to_slug=type_to_slug,
            author=get_default_author(db),
        ),
    )
