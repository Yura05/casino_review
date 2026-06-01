"""Jednorazowa migracja: dodaje bonusy typu 'match' (reload / match bonus) do 6 kasyn.

Match-bonus to procentowy bonus na powtorne depozyty (nie na pierwszy — to robi
'first_deposit'). Czesto: cotygodniowy, weekendowy, w okreslony dzien tygodnia.

Uruchomienie:
    python -m app.migrate_match_bonuses

Skrypt jest idempotentny: dla kazdego kasyna sprawdzamy, czy bonus typu
match juz istnieje. Jesli tak — pomijamy.

UWAGA: print() ASCII-only (cp1251 console crashuje na '₴').
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bonus, Casino


# (casino_slug, amount, wager, min_deposit, terms_uk, terms_ru)
_MATCH_DATA = [
    ("parimatch", "50% до 5 000 ₴ на другий депозит", "x35", "100 ₴",
     "Reload-бонус на другий депозит після завершення вітального пакета.",
     "Reload-бонус на второй депозит после завершения приветственного пакета."),
    ("cosmolot",  "75% до 2 000 ₴ щовівторка", "x35", "100 ₴",
     "Щотижневий вівторковий бонус для активних гравців з депозитом за останні 7 днів.",
     "Еженедельный вторничный бонус для активных игроков с депозитом за последние 7 дней."),
    ("pin-up",    "50% reload на вихідних до 3 000 ₴", "x35", "100 ₴",
     "Доступний кожних суботи й неділі. Активувати до першої ставки.",
     "Доступен каждую субботу и воскресенье. Активировать до первой ставки."),
    ("favbet",    "30% до 1 500 ₴ щотижня", "x30", "100 ₴",
     "Регулярний бонус, що оновлюється кожного понеділка.",
     "Регулярный бонус, обновляющийся каждый понедельник."),
    ("vbet",      "100% до 1 000 ₴ у перший понеділок місяця", "x35", "200 ₴",
     "Місячний reload для гравців, які зробили мінімум 1 депозит у попередньому місяці.",
     "Месячный reload для игроков, сделавших минимум 1 депозит в предыдущем месяце."),
    ("ggbet",     "50% + 25 фріспінів на третій депозит", "x40", "150 ₴",
     "Бонус-пакет на третій депозит у межах розширеної вітальної серії.",
     "Бонус-пакет на третий депозит в рамках расширенной приветственной серии."),
]


def run() -> None:
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        for slug, amount, wager, min_dep, terms_uk, terms_ru in _MATCH_DATA:
            casino = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if casino is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue

            existing = db.scalars(
                select(Bonus).where(
                    Bonus.casino_id == casino.id,
                    Bonus.type == "match",
                )
            ).first()
            if existing is not None:
                print(f"SKIP: {slug} juz ma bonus match")
                skipped += 1
                continue

            bonus = Bonus(
                casino_id=casino.id,
                type="match",
                amount=amount,
                wager=wager,
                min_deposit=min_dep,
                terms_uk=terms_uk,
                terms_ru=terms_ru,
            )
            db.add(bonus)
            print(f"ADD: {slug} -> match (wager {wager})")
            added += 1

        db.commit()
        print(f"OK: dodano {added}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
