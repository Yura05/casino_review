"""Router automatów do gry (slotów):
    /{lang}/igrovi-avtomaty/                — wszystkie sloty
    /{lang}/igrovi-avtomaty/bezkoshtovno/   — sloty za darmo (demo)
    /{lang}/slot/{slug}/                     — pojedynczy slot + gdzie grać
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_default_author, page_context, validate_lang
from app.models import Casino, Slot
from app.templating import templates

router = APIRouter()


def _published_slots(db: Session):
    return db.scalars(
        select(Slot).where(Slot.is_published.is_(True)).order_by(Slot.id)
    ).all()


@router.get("/{lang}/igrovi-avtomaty/")
def slot_index(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request=request,
        name="slot_list.html",
        context=page_context(request, lang, slots=_published_slots(db), free=False),
    )


@router.get("/{lang}/igrovi-avtomaty/bezkoshtovno/")
def slot_free(
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request=request,
        name="slot_list.html",
        context=page_context(request, lang, slots=_published_slots(db), free=True),
    )


@router.get("/{lang}/slot/{slug}/")
def slot_detail(
    slug: str,
    request: Request,
    lang: str = Depends(validate_lang),
    db: Session = Depends(get_db),
):
    slot = db.scalars(
        select(Slot).where(Slot.slug == slug, Slot.is_published.is_(True))
    ).first()
    if slot is None or slot.loc("name", lang) is None:
        raise HTTPException(status_code=404, detail="Slot not found")

    # "Gdzie grać" — najlepsze kasyna (slot dostępny w naszych ocenionych kasynach)
    casinos = db.scalars(
        select(Casino)
        .where(Casino.is_published.is_(True))
        .order_by(Casino.rating.desc())
        .options(selectinload(Casino.bonuses), selectinload(Casino.categories))
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="slot_detail.html",
        context=page_context(
            request, lang, slot=slot, casinos=casinos, author=get_default_author(db)
        ),
    )
