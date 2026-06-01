"""Jednorazowa migracja: dolacza Champion i Cosmobet do kategorii 'bez-verifikatsiyi'.

Uruchomienie:
    python -m app.migrate_bez_verifikatsiyi
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Casino, Category


def run() -> None:
    db = SessionLocal()
    try:
        cat = db.scalars(select(Category).where(Category.slug == "bez-verifikatsiyi")).first()
        if cat is None:
            print("ERROR: kategoria 'bez-verifikatsiyi' nie istnieje. Najpierw uruchom seed.")
            return

        for slug in ("champion", "cosmobet"):
            c = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if c is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue
            if cat in c.categories:
                print(f"SKIP: {slug} juz w kategorii bez-verifikatsiyi")
                continue
            c.categories.append(cat)
            print(f"ADD: {slug} -> bez-verifikatsiyi")

        db.commit()
        print("OK: migracja zakonczona")
    finally:
        db.close()


if __name__ == "__main__":
    run()
