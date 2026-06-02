"""Jednorazowa migracja: ustawia Slot.image dla istniejacych slotow.

Pliki SVG sa juz w static/img/slots/<slug>.svg, ale wczesniejszy seed nie
zapisywal kolumny image (dlatego karty slotow pokazywaly zielony placeholder
zamiast obrazka). Ten skrypt ustawia image = 'img/slots/<slug>.svg' dla
wierszy, w ktorych image jest puste.

Uruchomienie:
    .venv/bin/python -m app.migrate_slot_images   (na serwerze)
    python -m app.migrate_slot_images              (lokalnie)

Skrypt jest idempotentny: aktualizuje tylko wiersze z NULL/pustym image.

UWAGA: print() ASCII-only (konsola Windows cp1251 crashuje na non-ASCII).
"""

from sqlalchemy import text

from app.database import SessionLocal


def run() -> None:
    db = SessionLocal()
    try:
        r = db.execute(
            text(
                "UPDATE slot SET image = 'img/slots/' || slug || '.svg' "
                "WHERE image IS NULL OR image = ''"
            )
        )
        db.commit()
        print(f"OK: ustawiono image dla {r.rowcount} slotow")
    finally:
        db.close()


if __name__ == "__main__":
    run()
