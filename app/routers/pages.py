"""Router stron statycznych (treściowych): 18+, o nas, polityka prywatności.

Treść (długie teksty) trzymamy w osobnych szablonach na język:
templates/pages/<nazwa>_<lang>.html
"""

from fastapi import APIRouter, Depends, Request

from app.deps import page_context, validate_lang
from app.templating import templates

router = APIRouter()


def _render(name: str, request: Request, lang: str):
    return templates.TemplateResponse(
        request=request,
        name=f"pages/{name}_{lang}.html",
        context=page_context(request, lang),
    )


@router.get("/{lang}/18plus/")
def responsible(request: Request, lang: str = Depends(validate_lang)):
    return _render("responsible", request, lang)


@router.get("/{lang}/pro-nas/")
def about(request: Request, lang: str = Depends(validate_lang)):
    return _render("about", request, lang)


@router.get("/{lang}/privacy/")
def privacy(request: Request, lang: str = Depends(validate_lang)):
    return _render("privacy", request, lang)
