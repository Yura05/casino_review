"""Jednorazowa migracja: ustawia pole Slot.image na sciezke stylizowanej
okladki SVG (app/static/img/slots/<slug>.svg) dla kazdego slotu, ktory ma
odpowiadajacy plik na dysku.

Uruchomienie:
    python -m app.migrate_slot_covers

Skrypt jest idempotentny: pomija sloty bez pliku SVG lub z juz ustawionym
docelowym obrazem.

UWAGA: print() ASCII-only (cp1251 console crashuje na non-ASCII).
"""

from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Slot

_STATIC_DIR = Path(__file__).parent / "static"
_IMG_REL_DIR = "img/slots"


def run() -> None:
    db = SessionLocal()
    try:
        slots = db.scalars(select(Slot)).all()
        updated = 0
        skipped = 0
        for s in slots:
            rel_path = f"{_IMG_REL_DIR}/{s.slug}.svg"
            abs_path = _STATIC_DIR / rel_path
            if not abs_path.exists():
                print(f"SKIP: {s.slug} (brak pliku {rel_path})")
                skipped += 1
                continue
            if s.image == rel_path:
                print(f"SKIP: {s.slug} (image juz ustawione)")
                skipped += 1
                continue
            s.image = rel_path
            print(f"SET: {s.slug} -> {rel_path}")
            updated += 1

        db.commit()
        print(f"OK: zaktualizowano {updated}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
