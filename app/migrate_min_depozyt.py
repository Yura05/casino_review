"""Jednorazowa migracja: obniza min_deposit dla 3 kasyn i dolacza je do kategorii 'min-depozyt'.

Uruchomienie:
    python -m app.migrate_min_depozyt
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Casino, Category


def run() -> None:
    db = SessionLocal()
    try:
        # 1) Obnizamy min_deposit
        updates = {"ggbet": "50 ₴", "cosmobet": "75 ₴"}
        for slug, new_dep in updates.items():
            c = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if c is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue
            print(f"UPDATE {slug}: min_deposit {c.min_deposit!r} -> {new_dep!r}")
            c.min_deposit = new_dep

        # 2) Dolaczamy 3 kasyna do kategorii 'min-depozyt'
        cat = db.scalars(select(Category).where(Category.slug == "min-depozyt")).first()
        if cat is None:
            print("ERROR: kategoria 'min-depozyt' nie istnieje. Najpierw uruchom seed.")
            return

        for slug in ("ggbet", "cosmobet", "first"):
            c = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if c is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue
            if cat in c.categories:
                print(f"SKIP: {slug} juz w kategorii min-depozyt")
                continue
            c.categories.append(cat)
            print(f"ADD: {slug} -> min-depozyt")

        db.commit()
        print("OK: migracja zakonczona")
    finally:
        db.close()


if __name__ == "__main__":
    run()
