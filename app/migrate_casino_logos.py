"""Jednorazowa migracja: ustawia pole Casino.logo na sciezke stylizowanego
logo SVG (app/static/img/casinos/<slug>.svg) dla kazdego kasyna w bazie.

Uruchomienie:
    python -m app.migrate_casino_logos

Skrypt jest idempotentny: nadpisuje logo tylko jesli plik SVG istnieje,
a wartosc rozni sie od docelowej.

UWAGA: print() ASCII-only (cp1251 console crashuje na non-ASCII).
"""

from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Casino

# Katalog logo wzgledem /static oraz fizyczny katalog na dysku.
_STATIC_DIR = Path(__file__).parent / "static"
_LOGO_REL_DIR = "img/casinos"


def run() -> None:
    db = SessionLocal()
    try:
        casinos = db.scalars(select(Casino)).all()
        updated = 0
        skipped = 0
        for c in casinos:
            rel_path = f"{_LOGO_REL_DIR}/{c.slug}.svg"
            abs_path = _STATIC_DIR / rel_path
            if not abs_path.exists():
                print(f"SKIP: {c.slug} (brak pliku {rel_path})")
                skipped += 1
                continue
            if c.logo == rel_path:
                print(f"SKIP: {c.slug} (logo juz ustawione)")
                skipped += 1
                continue
            c.logo = rel_path
            print(f"SET: {c.slug} -> {rel_path}")
            updated += 1

        db.commit()
        print(f"OK: zaktualizowano {updated}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
