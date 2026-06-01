"""Współdzielone domieszki (mixiny) dla modeli."""


class LocalizedMixin:
    """Dostęp do pól zależnych od języka.

    Zamiast pisać `casino.description_uk` / `casino.description_ru`,
    w szablonie używamy: `casino.loc('description', lang)`.
    """

    def loc(self, field: str, lang: str):
        return getattr(self, f"{field}_{lang}", None)
