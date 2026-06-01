"""Jednorazowa migracja: ustawia pole Bookmaker.logo na sciezke stylizowanego
logo SVG (app/static/img/bookmakers/<slug>.svg) dla kazdego bukmachera,
ktory ma odpowiadajacy plik na dysku, a nie ma jeszcze logo.

Uruchomienie:
    python -m app.migrate_bookmaker_logos

Skrypt jest idempotentny: pomija bukmacherow bez pliku SVG lub z juz
ustawionym docelowym logo.

UWAGA: print() ASCII-only (cp1251 console crashuje na non-ASCII).
"""

from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bookmaker

_STATIC_DIR = Path(__file__).parent / "static"
_LOGO_REL_DIR = "img/bookmakers"


def run() -> None:
    db = SessionLocal()
    try:
        bookmakers = db.scalars(select(Bookmaker)).all()
        updated = 0
        skipped = 0
        for b in bookmakers:
            rel_path = f"{_LOGO_REL_DIR}/{b.slug}.svg"
            abs_path = _STATIC_DIR / rel_path
            if not abs_path.exists():
                print(f"SKIP: {b.slug} (brak pliku {rel_path})")
                skipped += 1
                continue
            if b.logo == rel_path:
                print(f"SKIP: {b.slug} (logo juz ustawione)")
                skipped += 1
                continue
            b.logo = rel_path
            print(f"SET: {b.slug} -> {rel_path}")
            updated += 1

        db.commit()
        print(f"OK: zaktualizowano {updated}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
