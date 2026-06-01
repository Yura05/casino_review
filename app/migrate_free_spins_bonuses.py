"""Jednorazowa migracja: dodaje bonusy typu 'free_spins' (jako oddzielny typ — np.
cotygodniowe darmowe spiny / promocje weekendowe) do 6 kasyn.

To NIE sa fri-spiny z bonusu rejestracyjnego (te juz sa zapisane jako 'registration').
To osobny typ — promo-spiny dostepne dla zarejestrowanych graczy regularnie.

Uruchomienie:
    python -m app.migrate_free_spins_bonuses

Skrypt jest idempotentny: dla kazdego kasyna sprawdzamy, czy bonus typu
free_spins juz istnieje. Jesli tak — pomijamy.

UWAGA: print() zostaje ASCII-only (cp1251 console crashuje na '₴'/'—').
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Bonus, Casino


# (casino_slug, amount, wager, min_deposit, terms_uk, terms_ru)
# Promo-FS dla aktywnych graczy. Wymagaja zwykle niewielkiego depozytu (50-200 ₴).
_FREE_SPINS_DATA = [
    ("parimatch", "200 фріспінів на Big Bass Bonanza", "x35", "200 ₴",
     "Активуються після поповнення від 200 ₴. Доступні протягом 5 днів.",
     "Активируются после пополнения от 200 ₴. Доступны в течение 5 дней."),
    ("cosmolot",  "150 фріспінів на Sweet Bonanza", "x35", "100 ₴",
     "Пакет фріспінів видається партіями по 50 шт. у наступні 3 дні.",
     "Пакет фриспинов выдаётся партиями по 50 шт. в следующие 3 дня."),
    ("pin-up",    "100 фріспінів на Gates of Olympus", "x40", "100 ₴",
     "Промо-фріспіни для гравців, які поповнили рахунок за останні 7 днів.",
     "Промо-фриспины для игроков, пополнивших счёт за последние 7 дней."),
    ("vbet",      "75 фріспінів на Book of Dead", "x35", "100 ₴",
     "Активуються одразу після поповнення. Термін відіграшу — 7 днів.",
     "Активируются сразу после пополнения. Срок отыгрыша — 7 дней."),
    ("slotoking", "120 фріспінів щовихідних", "x40", "150 ₴",
     "Видаються кожних вихідних активним гравцям з депозитом від 150 ₴.",
     "Выдаются каждые выходные активным игрокам с депозитом от 150 ₴."),
    ("ggbet",     "50 фріспінів щотижня", "x35", "50 ₴",
     "Регулярний тижневий бонус для гравців, які грали 3+ дні на тиждень.",
     "Регулярный недельный бонус для игроков, игравших 3+ дня в неделю."),
]


def run() -> None:
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        for slug, amount, wager, min_dep, terms_uk, terms_ru in _FREE_SPINS_DATA:
            casino = db.scalars(select(Casino).where(Casino.slug == slug)).first()
            if casino is None:
                print(f"SKIP: kasyno {slug} nie znalezione")
                continue

            existing = db.scalars(
                select(Bonus).where(
                    Bonus.casino_id == casino.id,
                    Bonus.type == "free_spins",
                )
            ).first()
            if existing is not None:
                print(f"SKIP: {slug} juz ma bonus free_spins")
                skipped += 1
                continue

            bonus = Bonus(
                casino_id=casino.id,
                type="free_spins",
                amount=amount,
                wager=wager,
                min_deposit=min_dep,
                terms_uk=terms_uk,
                terms_ru=terms_ru,
            )
            db.add(bonus)
            # ASCII-only print (amount/min_dep zawieraja '₴'/'—').
            print(f"ADD: {slug} -> free_spins (wager {wager})")
            added += 1

        db.commit()
        print(f"OK: dodano {added}, pominieto {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
