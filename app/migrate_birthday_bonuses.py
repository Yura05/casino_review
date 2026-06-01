"""Jednorazowa migracja: dodaje bonusy typu 'birthday' (urodzinowe) do 5 kasyn.

Bonus urodzinowy to indywidualny prezent dla graczy z zweryfikowanym kontem
(DOB potwierdzona) i pewnym poziomem aktywnosci. Wielkosc zalezy zwykle od
statusu w programie lojalnosciowym.

Uruchomienie:
    python -m app.migrate_birthday_bonuses

Skrypt jest idempotentny: dla kazdego kasyna sprawdzamy, czy bonus typu
birthday juz istnieje. Jesli tak — pomijamy.

UWAGA: print() ASCII-only (cp1251 console crashuje na '₴'/'—').
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bonus, Casino


# (casino_slug, amount, wager, min_deposit, terms_uk, terms_ru)
# Wager niski (x25-x35) — to "prezent", a nie regularna oferta.
_BIRTHDAY_DATA = [
    ("parimatch", "100% до 3 000 ₴ у день народження", "x30", "100 ₴",
     "Доступно гравцям з підтвердженою датою народження та поповненням за останні 60 днів.",
     "Доступно игрокам с подтверждённой датой рождения и пополнением за последние 60 дней."),
    ("cosmolot",  "100 фріспінів у місяць народження", "x35", "50 ₴",
     "Фріспіни на Sweet Bonanza. Активуються протягом місяця народження.",
     "Фриспины на Sweet Bonanza. Активируются в течение месяца рождения."),
    ("pin-up",    "50 фріспінів + 500 ₴ подарунок", "x30", "100 ₴",
     "Подарунковий пакет для активних гравців у тиждень дня народження.",
     "Подарочный пакет для активных игроков в неделю дня рождения."),
    ("favbet",    "Фрібет 200 ₴ без вейджеру", "x25", "—",
     "Безкоштовна ставка у день народження. Виграш зараховується без додаткових умов.",
     "Бесплатная ставка в день рождения. Выигрыш зачисляется без дополнительных условий."),
    ("slotoking", "150 фріспінів + кешбек 10%", "x35", "100 ₴",
     "Комбінований святковий пакет із кешбеком на тижневі програші.",
     "Комбинированный праздничный пакет с кешбеком на недельные проигрыши."),
]


def run() -> None:
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        for slug, amount, wager, min_dep, terms_uk, terms_ru in _BIRTHDAY_DATA:
            casino = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if casino is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue

            existing = db.scalars(
                select(Bonus).where(
                    Bonus.casino_id == casino.id,
                    Bonus.type == "birthday",
                )
            ).first()
            if existing is not None:
                print(f"SKIP: {slug} juz ma bonus birthday")
                skipped += 1
                continue

            bonus = Bonus(
                casino_id=casino.id,
                type="birthday",
                amount=amount,
                wager=wager,
                min_deposit=min_dep,
                terms_uk=terms_uk,
                terms_ru=terms_ru,
            )
            db.add(bonus)
            print(f"ADD: {slug} -> birthday (wager {wager})")
            added += 1

        db.commit()
        print(f"OK: dodano {added}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
