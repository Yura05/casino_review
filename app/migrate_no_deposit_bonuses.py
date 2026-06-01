"""Jednorazowa migracja: dodaje bonusy typu 'no_deposit' do 5 top-kasyn.

Uruchomienie:
    python -m app.migrate_no_deposit_bonuses

Skrypt jest idempotentny: dla kazdego kasyna sprawdzamy, czy bonus typu
no_deposit juz istnieje. Jesli tak — pomijamy. Jesli nie — dodajemy.
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bonus, Casino


# (casino_slug, amount, wager, terms_uk, terms_ru)
# Pole `amount` w modelu Bonus jest jezykowo-neutralne (jak w seed.py) — uzywamy UK.
_NO_DEPOSIT_DATA = [
    ("parimatch", "50 FS без депозиту", "x40",
     "Фріспіни нараховуються після підтвердження email. Без поповнення рахунку.",
     "Фриспины начисляются после подтверждения email. Без пополнения счёта."),
    ("cosmolot",  "25 FS без депозиту", "x40",
     "Фріспіни активуються одразу після реєстрації. Максимальний виграш обмежений.",
     "Фриспины активируются сразу после регистрации. Максимальный выигрыш ограничен."),
    ("pin-up",    "30 FS без депозиту", "x45",
     "Фріспіни доступні на популярних слотах від Pragmatic Play.",
     "Фриспины доступны на популярных слотах от Pragmatic Play."),
    ("favbet",    "20 FS без депозиту", "x40",
     "Фріспіни нараховуються після підтвердження номеру телефону.",
     "Фриспины начисляются после подтверждения номера телефона."),
    ("slotoking", "50 FS без депозиту", "x45",
     "Фріспіни видаються партіями по 10 штук протягом 5 днів.",
     "Фриспины выдаются партиями по 10 штук в течение 5 дней."),
]


def run() -> None:
    db = SessionLocal()
    try:
        for slug, amount, wager, terms_uk, terms_ru in _NO_DEPOSIT_DATA:
            casino = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if casino is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue

            existing = db.scalars(
                select(Bonus).where(
                    Bonus.casino_id == casino.id,
                    Bonus.type == "no_deposit",
                )
            ).first()
            if existing is not None:
                print(f"SKIP: {slug} juz ma bonus no_deposit")
                continue

            bonus = Bonus(
                casino_id=casino.id,
                type="no_deposit",
                amount=amount,
                wager=wager,
                min_deposit="—",
                terms_uk=terms_uk,
                terms_ru=terms_ru,
            )
            db.add(bonus)
            print(f"ADD: {slug} -> no_deposit ({amount}, wager {wager})")

        db.commit()
        print("OK: migracja zakonczona")
    finally:
        db.close()


if __name__ == "__main__":
    run()
