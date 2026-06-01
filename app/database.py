"""Konfiguracja SQLAlchemy: silnik (engine), fabryka sesji i klasa bazowa modeli.

Modele (krok 2) będą dziedziczyć po `Base`.
W endpointach używamy `Depends(get_db)`, aby otrzymać sesję bazy danych.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # sprawdza połączenie przed użyciem (unika "stale connections")
    echo=settings.debug,  # loguje zapytania SQL w trybie debug
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Klasa bazowa dla wszystkich modeli ORM (SQLAlchemy 2.0, styl typowany)."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Zależność FastAPI: otwiera sesję na czas requestu i zamyka po jego zakończeniu."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
