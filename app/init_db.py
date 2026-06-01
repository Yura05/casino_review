"""Tworzenie tabel w bazie danych na podstawie modeli.

Uruchomienie (po skonfigurowaniu .env i utworzeniu bazy 'casino_review'):
    python -m app.init_db

UWAGA: na tym etapie używamy create_all (proste, bez migracji).
Gdy schemat zacznie się zmieniać, wprowadzimy Alembic (migracje).
"""

from app.database import Base, engine
from app import models  # noqa: F401  — import rejestruje wszystkie modele w Base.metadata


def main() -> None:
    print("Tworze tabele...")
    Base.metadata.create_all(bind=engine)
    tables = ", ".join(sorted(Base.metadata.tables))
    print(f"Gotowe. Tabele: {tables}")


if __name__ == "__main__":
    main()
