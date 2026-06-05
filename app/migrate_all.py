"""Uruchamia WSZYSTKIE migracje danych po kolei (idempotentnie).

Po co: swiezo postawiony serwer ma tylko podstawowy seed (init_db + seed),
a duzo danych (bonusy typow no_deposit/free_spins/birthday/match, dodatkowi
bukmacherzy, kategorie min-depozyt/bez-verifikatsiyi, logo/obrazki) zyje w
osobnych skryptach migracyjnych. Ten plik odpala je wszystkie w poprawnej
kolejnosci, dzieki czemu serwer dogania stan lokalny i puste strony
(np. /bonusy/no-deposit/) dostaja karty.

Uruchomienie:
    .venv/bin/python -m app.migrate_all   (serwer)
    python -m app.migrate_all              (lokalnie)

Kazda migracja jest idempotentna (pomija to, co juz istnieje), wiec skrypt
mozna uruchamiac wielokrotnie bezpiecznie. Bledy pojedynczej migracji nie
zatrzymuja reszty.

UWAGA: print() ASCII-only (konsola Windows cp1251 crashuje na non-ASCII).
"""

import importlib
import sys

# Migracje skladowe drukuja non-ASCII (np. '₴', '—'). Na konsoli Windows cp1251
# to crashuje — wymuszamy UTF-8, by skrypt dzialal na kazdej konsoli.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

# Kolejnosc WAZNA:
#  - bonus_fields: kolumny (na wszelki wypadek; na swiezej bazie i tak sa)
#  - more_bookmakers PRZED victorbet_kibersport (victorbet musi istniec)
#  - kategorie i bonusy: po tym, jak kasyna/bukmacherzy istnieja
#  - logo/obrazki na koncu (uzupelniaja istniejace wiersze)
_MIGRATIONS = [
    "migrate_bonus_fields",
    "migrate_more_bookmakers",
    "migrate_victorbet_kibersport",
    "migrate_min_depozyt",
    "migrate_bez_verifikatsiyi",
    "migrate_no_deposit_bonuses",
    "migrate_registration_bonuses",
    "migrate_free_spins_bonuses",
    "migrate_birthday_bonuses",
    "migrate_match_bonuses",
    "migrate_casino_logos",
    "migrate_bookmaker_logos",
    "migrate_slot_images",
    "migrate_slot_covers",
    "migrate_casino_badges",
]


def run() -> None:
    ok = 0
    failed = 0
    for name in _MIGRATIONS:
        print(f"\n===== {name} =====")
        try:
            mod = importlib.import_module(f"app.{name}")
            mod.run()
            ok += 1
        except Exception as exc:  # noqa: BLE001 — chcemy isc dalej mimo bledu
            print(f"ERROR in {name}: {exc!r}")
            failed += 1
    print(f"\n========== DONE: {ok} ok, {failed} failed ==========")


if __name__ == "__main__":
    run()
