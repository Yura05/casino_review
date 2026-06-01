"""Punkt wejścia aplikacji FastAPI.

Uruchomienie (dev):
    uvicorn app.main:app --reload

Adresy:
    /            -> przekierowanie na /uk/ (język domyślny)
    /uk/  /ru/   -> strona główna w danym języku
    /health      -> health check
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.i18n import DEFAULT_LANG
from app.routers import (
    author,
    blog,
    bonus,
    bookmaker,
    casino,
    category,
    home,
    pages,
    payment,
    seo,
    slot,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=settings.site_name, debug=settings.debug)

# Pliki statyczne (CSS / JS / obrazy) dostępne pod /static/...
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Routery
app.include_router(home.router)
app.include_router(casino.router)
app.include_router(category.router)
app.include_router(bonus.router)
app.include_router(bookmaker.router)
app.include_router(slot.router)
app.include_router(blog.router)
app.include_router(payment.router)
app.include_router(author.router)
app.include_router(pages.router)
app.include_router(seo.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url=f"/{DEFAULT_LANG}/")
