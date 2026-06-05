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
    """Lekki markdown -> ostylowany HTML dla dlugich recenzji i artykulow.

    Obsluguje:
      `## ` -> <h2>, `### ` -> <h3>,
      `- ` -> lista <ul><li>, `1. ` -> lista numerowana <ol><li>,
      tabele markdown (| a | b | + wiersz `|---|---|`),
      `**pogrubienie**`, akapity (linie oddzielone pusta linia).

    Tresc jest AUTORSKA (z naszej bazy, nie od uzytkownika), wiec zwracamy
    Markup. Tekst i tak escapujemy, by uniknac przypadkowego HTML.
    """
    if not text:
        return Markup("")

    def inline(s: str) -> str:
        s = str(escape(s))
        return re.sub(r"\*\*(.+?)\*\*", r'<strong class="font-semibold text-slate-900">\1</strong>', s)

    def cells(row: str) -> list[str]:
        return [c.strip() for c in row.strip().strip("|").split("|")]

    out: list[str] = []
    para: list[str] = []
    list_type: str | None = None  # None | "ul" | "ol"

    def flush_para() -> None:
        if para:
            out.append('<p class="mt-3 text-slate-700 leading-relaxed">' + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    lines = text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        nxt = lines[i + 1].strip() if i + 1 < n else ""

        # --- Tabela: naglowek '| a | b |' + separator '|---|---|' ---
        if (
            line.startswith("|")
            and nxt.startswith("|")
            and set(nxt) <= set("|-: ")
            and "-" in nxt
        ):
            flush_para(); close_list()
            header = cells(line)
            rows: list[list[str]] = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            thead = "".join(
                f'<th class="p-3 border-b border-slate-200 font-semibold">{inline(h)}</th>' for h in header
            )
            tbody = "".join(
                "<tr>" + "".join(
                    f'<td class="p-3 border-b border-slate-100 align-top">{inline(c)}</td>' for c in row
                ) + "</tr>"
                for row in rows
            )
            out.append(
                '<div class="mt-4 overflow-x-auto"><table class="w-full text-sm text-left border border-slate-200">'
                f'<thead><tr class="bg-slate-100 text-slate-700">{thead}</tr></thead>'
                f'<tbody class="text-slate-700">{tbody}</tbody></table></div>'
            )
            continue

        if not line:
            flush_para(); close_list()
        elif line.startswith("### "):
            flush_para(); close_list()
            out.append('<h3 class="mt-6 mb-1 font-bold text-slate-900">' + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush_para(); close_list()
            out.append('<h2 class="mt-8 mb-2 text-xl font-bold text-slate-900">' + inline(line[3:]) + "</h2>")
        elif line.startswith("- "):
            flush_para()
            if list_type != "ul":
                close_list()
                out.append('<ul class="mt-3 space-y-1 list-disc pl-5 text-slate-700 leading-relaxed">')
                list_type = "ul"
            out.append("<li>" + inline(line[2:]) + "</li>")
        elif re.match(r"^\d+\.\s", line):
            flush_para()
            if list_type != "ol":
                close_list()
                out.append('<ol class="mt-3 space-y-1 list-decimal pl-5 text-slate-700 leading-relaxed">')
                list_type = "ol"
            out.append("<li>" + inline(re.sub(r"^\d+\.\s", "", line)) + "</li>")
        else:
            para.append(line)
        i += 1

    flush_para()
    close_list()
    return Markup("".join(out))


templates.env.filters["richtext"] = _richtext
