"""Wspólna instancja szablonów Jinja2 — importowana przez routery i main.

Wydzielona do osobnego modułu, aby routery nie musiały importować `main`
(co tworzyłoby cykliczny import).
"""

from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _asset_v(rel_path: str) -> str:
    """Zwraca mtime pliku statycznego jako string — do cache-bustingu (`?v=...`)."""
    p = BASE_DIR / "static" / rel_path
    try:
        return str(int(p.stat().st_mtime))
    except OSError:
        return "0"


templates.env.globals["asset_v"] = _asset_v


def _paragraphs(text: str | None) -> list[str]:
    """Dzieli tekst na akapity po pustej linii (do dłuższych sekcji)."""
    if not text:
        return []
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def _lines(text: str | None) -> list[str]:
    """Dzieli tekst na pojedyncze linie (do list zalet/wad)."""
    if not text:
        return []
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


templates.env.filters["paragraphs"] = _paragraphs
templates.env.filters["lines"] = _lines
