"""Popularne kasyna w Ukrainie — do bloku porównania na stronie recenzji.

UWAGA: to realne marki (legalne kasyna w Ukrainie, lista wzorowana na
legalactivity.com.ua). Każde ma własną stronę recenzji /casino/{slug}/.
Wartości bonusów/ocen są PRZYKŁADOWE (placeholder) — przed publikacją zweryfikuj.
"""

POPULAR_UA_CASINOS: list[dict] = [
    {"name": "Cosmolot", "slug": "cosmolot", "rating": 4.6, "bonus": "100% + 50 FS", "license": "КРАІЛ"},
    {"name": "PariMatch", "slug": "parimatch", "rating": 4.7, "bonus": "150% до 45 000 ₴", "license": "КРАІЛ"},
    {"name": "Favbet", "slug": "favbet", "rating": 4.5, "bonus": "100% до 20 000 ₴", "license": "КРАІЛ"},
    {"name": "VBET", "slug": "vbet", "rating": 4.5, "bonus": "100% до 30 000 ₴", "license": "КРАІЛ"},
    {"name": "GGBet", "slug": "ggbet", "rating": 4.4, "bonus": "100% + 100 FS", "license": "КРАІЛ"},
    {"name": "Pin-Up", "slug": "pin-up", "rating": 4.6, "bonus": "150% + 250 FS", "license": "КРАІЛ"},
    {"name": "Cosmobet", "slug": "cosmobet", "rating": 4.4, "bonus": "120% до 15 000 ₴", "license": "КРАІЛ"},
    {"name": "First", "slug": "first", "rating": 4.3, "bonus": "100% до 10 000 ₴", "license": "КРАІЛ"},
    {"name": "Slotoking", "slug": "slotoking", "rating": 4.5, "bonus": "175% + 70 FS", "license": "КРАІЛ"},
    {"name": "Champion", "slug": "champion", "rating": 4.4, "bonus": "100% + 100 FS", "license": "КРАІЛ"},
]


def competitors_for(casino_id: int, current_slug: str | None = None, n: int = 4) -> list[dict]:
    """Wybiera n konkurentów (z wyłączeniem bieżącego kasyna).
    Zestaw różni się dla różnych kasyn dzięki offsetowi wg id."""
    pool = [c for c in POPULAR_UA_CASINOS if c["slug"] != current_slug]
    start = (casino_id * 3) % len(pool)
    return [pool[(start + i) % len(pool)] for i in range(n)]
