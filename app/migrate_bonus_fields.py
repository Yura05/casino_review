"""Jednorazowa migracja: dodaje kolumny wager i min_deposit do tabeli bonus
oraz wypelnia je rozsadnymi wartosciami domyslnymi dla istniejacych rekordow.

Uruchomienie:
    python -m app.migrate_bonus_fields

Skrypt jest idempotentny: ALTER TABLE uzywa IF NOT EXISTS, a UPDATE
nadpisuje tylko NULL-e (nie ruszy juz wypelnionych wartosci).
"""

from sqlalchemy import text

from app.database import SessionLocal, engine


_DDL_STATEMENTS = (
    "ALTER TABLE bonus ADD COLUMN IF NOT EXISTS wager VARCHAR(50)",
    "ALTER TABLE bonus ADD COLUMN IF NOT EXISTS min_deposit VARCHAR(50)",
)


def run() -> None:
    # 1) DDL — kolumny dodajemy poza transakcja sesji (engine.begin -> autocommit DDL).
    with engine.begin() as conn:
        for sql in _DDL_STATEMENTS:
            conn.execute(text(sql))
            print(f"OK DDL: {sql}")

    # 2) Dane — uzupelniamy NULL-owe wartosci sensownymi domyslnymi.
    db = SessionLocal()
    try:
        # first_deposit: wager x35, min_deposit = min_deposit kasyna
        r1 = db.execute(text("""
            UPDATE bonus AS b
            SET wager = 'x35',
                min_deposit = c.min_deposit
            FROM casino AS c
            WHERE b.casino_id = c.id
              AND b.type = 'first_deposit'
              AND (b.wager IS NULL OR b.min_deposit IS NULL)
        """))
        print(f"UPDATE first_deposit: {r1.rowcount} wierszy")

        # registration: wager x40, min_deposit = nie dotyczy
        r2 = db.execute(text("""
            UPDATE bonus
            SET wager = COALESCE(wager, 'x40'),
                min_deposit = COALESCE(min_deposit, '—')
            WHERE type = 'registration'
              AND (wager IS NULL OR min_deposit IS NULL)
        """))
        print(f"UPDATE registration: {r2.rowcount} wierszy")

        # Pozostale typy (no_deposit, free_spins, birthday, match) — gdyby cos juz bylo:
        r3 = db.execute(text("""
            UPDATE bonus
            SET wager = COALESCE(wager, 'x40'),
                min_deposit = COALESCE(min_deposit, '—')
            WHERE type IN ('no_deposit', 'free_spins', 'birthday', 'match')
              AND (wager IS NULL OR min_deposit IS NULL)
        """))
        print(f"UPDATE pozostale typy: {r3.rowcount} wierszy")

        db.commit()
        print("OK: migracja zakonczona")
    finally:
        db.close()


if __name__ == "__main__":
    run()
