"""Jednorazowa migracja: roznicuje istniejace bonusy typu 'registration' (po seed
wszystkie maja 25 FS) na realistyczne, zroznicowane propozycje per kasyno.

Uruchomienie:
    python -m app.migrate_registration_bonuses

Skrypt jest idempotentny: aktualizuje rekord tylko jesli amount = '25 FS'
(czyli oryginalna wartosc z seeda). Jesli juz cos zmieniono recznie — pomija.
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bonus, Casino


# (casino_slug, amount, wager, terms_uk, terms_ru)
# Roznicujemy: niektore kasyna daja tylko FS, niektore tylko kase, niektore mix.
_REGISTRATION_DATA = [
    ("parimatch", "50 фріспінів на Book of Dead", "x40",
     "Фріспіни нараховуються після підтвердження email. Слот Book of Dead.",
     "Фриспины начисляются после подтверждения email. Слот Book of Dead."),
    ("cosmolot",  "25 фріспінів + 50 ₴", "x40",
     "Комбінований бонус після завершення реєстрації. Фріспіни на Sweet Bonanza.",
     "Комбинированный бонус после завершения регистрации. Фриспины на Sweet Bonanza."),
    ("pin-up",    "30 фріспінів на Sweet Bonanza", "x40",
     "Фріспіни активуються після підтвердження номеру телефону.",
     "Фриспины активируются после подтверждения номера телефона."),
    ("favbet",    "100 ₴ на бонусний рахунок", "x35",
     "Гроші зараховуються після підтвердження email і номеру телефону.",
     "Деньги зачисляются после подтверждения email и номера телефона."),
    ("vbet",      "20 фріспінів на Gates of Olympus", "x40",
     "Фріспіни на популярний слот від Pragmatic Play.",
     "Фриспины на популярный слот от Pragmatic Play."),
    ("slotoking", "40 фріспінів на Book of Ra", "x40",
     "Фріспіни нараховуються партіями по 10 штук протягом 4 днів.",
     "Фриспины начисляются партиями по 10 штук в течение 4 дней."),
    ("ggbet",     "25 фріспінів + 25 ₴", "x35",
     "Комбінований стартовий бонус для нових гравців.",
     "Комбинированный стартовый бонус для новых игроков."),
    ("cosmobet",  "50 фріспінів", "x45",
     "Фріспіни доступні на популярних слотах від NetEnt і Pragmatic Play.",
     "Фриспины доступны на популярных слотах от NetEnt и Pragmatic Play."),
    ("champion",  "100 ₴ + 20 фріспінів", "x35",
     "Бонус активується після підтвердження email і номеру телефону.",
     "Бонус активируется после подтверждения email и номера телефона."),
    ("first",     "75 ₴ після підтвердження телефону", "x35",
     "Невелика грошова винагорода для нових українських гравців.",
     "Небольшое денежное вознаграждение для новых украинских игроков."),
]


def run() -> None:
    db = SessionLocal()
    try:
        updated = 0
        skipped = 0
        for slug, amount, wager, terms_uk, terms_ru in _REGISTRATION_DATA:
            casino = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if casino is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue

            bonus = db.scalars(
                select(Bonus).where(
                    Bonus.casino_id == casino.id,
                    Bonus.type == "registration",
                )
            ).first()
            if bonus is None:
                print(f"SKIP: {slug} nie ma bonusu registration")
                continue

            # Idempotencja: zmieniamy tylko jesli to oryginalna seed-owa wartosc.
            if bonus.amount != "25 FS":
                # Nie wypisujemy `bonus.amount` (moze zawierac znaki spoza cp1251).
                print(f"SKIP: {slug} ma juz zmodyfikowany bonus")
                skipped += 1
                continue

            bonus.amount = amount
            bonus.wager = wager
            bonus.terms_uk = terms_uk
            bonus.terms_ru = terms_ru
            # UWAGA: nie wypisujemy `amount`/`terms_*` (moga zawierac znaki spoza cp1251,
            # np. '₴'/'—', co wywola UnicodeEncodeError w konsoli Windows).
            print(f"UPDATE: {slug} (wager {wager})")
            updated += 1

        db.commit()
        print(f"OK: zaktualizowano {updated}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
