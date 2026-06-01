"""Jednorazowa migracja: dolacza VictorBet do kategorii zakladow 'kibersport'.

VictorBet to multi-sport BK z szeroka linia (futbol, basketbol, boks, sport).
Logicznie powinien tez pokrywac kibersport — co rozsadnie pasuje do profilu
"szeroki wybor dla nowicjusza".

Uruchomienie:
    python -m app.migrate_victorbet_kibersport

UWAGA: print() ASCII-only (cp1251 console).
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import BettingCategory, Bookmaker


def run() -> None:
    db = SessionLocal()
    try:
        bk = db.scalars(select(Bookmaker).where(Bookmaker.slug == "victorbet")).first()
        if bk is None:
            print("ERROR: bukmacher victorbet nie znaleziony")
            return

        cat = db.scalars(select(BettingCategory).where(BettingCategory.slug == "kibersport")).first()
        if cat is None:
            print("ERROR: kategoria kibersport nie znaleziona")
            return

        if cat in bk.betting_categories:
            print("SKIP: VictorBet juz w kategorii kibersport")
            return

        bk.betting_categories.append(cat)
        db.commit()
        print("OK: dolaczono VictorBet do kategorii kibersport")
    finally:
        db.close()


if __name__ == "__main__":
    run()
