"""Wspólna instancja szablonów Jinja2 — importowana przez routery i main.

Wydzielona do osobnego modułu, aby routery nie musiały importować `main`
(co tworzyłoby cykliczny import).
"""

import re
from pathlib import Path

from fastapi.templating import Jinja2Templates
from markupsafe import Markup, escape

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


def _richtext(text: str | None) -> Markup:
    """Lekki markdown -> ostylowany HTML dla dlugich recenzji.

    Obsluguje:
      `## ` -> <h2>, `### ` -> <h3>, `- ` -> lista <ul><li>,
      `**pogrubienie**`, akapity (linie oddzielone pusta linia).

    Tresc jest AUTORSKA (z naszej bazy, nie od uzytkownika), wiec zwracamy
    Markup. Tekst i tak escapujemy, by uniknac przypadkowego HTML.
    """
    if not text:
        return Markup("")

    def inline(s: str) -> str:
        s = str(escape(s))
        return re.sub(r"\*\*(.+?)\*\*", r'<strong class="font-semibold text-slate-900">\1</strong>', s)

    out: list[str] = []
    para: list[str] = []
    in_list = False

    def flush_para() -> None:
        if para:
            out.append('<p class="mt-3 text-slate-700 leading-relaxed">' + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            flush_para()
            close_list()
        elif line.startswith("### "):
            flush_para(); close_list()
            out.append('<h3 class="mt-6 mb-1 font-bold text-slate-900">' + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush_para(); close_list()
            out.append('<h2 class="mt-8 mb-2 text-xl font-bold text-slate-900">' + inline(line[3:]) + "</h2>")
        elif line.startswith("- "):
            flush_para()
            if not in_list:
                out.append('<ul class="mt-3 space-y-1 list-disc pl-5 text-slate-700 leading-relaxed">')
                in_list = True
            out.append("<li>" + inline(line[2:]) + "</li>")
        else:
            para.append(line)

    flush_para()
    close_list()
    return Markup("".join(out))


templates.env.filters["richtext"] = _richtext
