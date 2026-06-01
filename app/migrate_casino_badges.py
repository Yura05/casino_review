"""Jednorazowa migracja: dodaje kolumne Casino.badges (CSV kluczy bejdzy)
oraz wypelnia ja przykladowymi wartosciami dla istniejacych kasyn (po slug).

Uruchomienie:
    python -m app.migrate_casino_badges

Skrypt jest idempotentny: ALTER TABLE uzywa IF NOT EXISTS, a UPDATE
ustawia badges tylko gdy kolumna jest NULL (nie nadpisuje recznych zmian).

Klucze bejdzy (renderowane w macro casino_badges): top, editor, fast,
exclusive, new, popular, bonus, mobile. Etykiety dwujezyczne -> i18n (badge_*).

UWAGA: print() ASCII-only (cp1251 console crashuje na non-ASCII).
"""

from sqlalchemy import text

from app.database import SessionLocal, engine

# Przykladowe (placeholder) przypisanie bejdzy po slug kasyna.
_BADGES = {
    "cosmolot": "popular",
    "parimatch": "top,fast",
    "favbet": "editor",
    "ggbet": "new",
    "pin-up": "bonus,fast",
    "cosmobet": "new",
    "champion": "fast",
}


def run() -> None:
    # 1) DDL — kolumna poza transakcja sesji (autocommit DDL).
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE casino ADD COLUMN IF NOT EXISTS badges VARCHAR(120)"))
        print("OK DDL: ALTER TABLE casino ADD COLUMN IF NOT EXISTS badges")

    # 2) Dane — ustawiamy badges tylko dla NULL-owych wierszy (idempotentnie).
    db = SessionLocal()
    try:
        updated = 0
        for slug, badges in _BADGES.items():
            r = db.execute(
                text(
                    "UPDATE casino SET badges = :b "
                    "WHERE slug = :s AND badges IS NULL"
                ),
                {"b": badges, "s": slug},
            )
            if r.rowcount:
                print(f"SET: {slug} -> {badges}")
                updated += r.rowcount
            else:
                print(f"SKIP: {slug} (brak wiersza lub badges juz ustawione)")
        db.commit()
        print(f"OK: zaktualizowano {updated} wierszy")
    finally:
        db.close()


if __name__ == "__main__":
    run()
