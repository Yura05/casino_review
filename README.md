# Casino Review

Serwis z recenzjami i rankingami kasyn online. Renderowanie po stronie serwera
(FastAPI + Jinja2) z myślą o SEO.

## Stack

- **Backend:** Python + FastAPI
- **Szablony:** Jinja2 (server-side rendering)
- **Frontend:** HTML + Tailwind CSS + Vanilla JS
- **Baza danych:** PostgreSQL + SQLAlchemy
- **Hosting:** Railway / Render

## Struktura projektu

```
app/
├── main.py          # punkt wejścia FastAPI, montuje static + szablony, routing
├── config.py        # ustawienia z .env (pydantic-settings)
├── database.py      # engine, sesja, Base (SQLAlchemy)
├── i18n.py          # języki (uk/ru), tłumaczenia UI, helpery URL-i językowych
├── deps.py          # validate_lang + page_context (wspólny kontekst szablonów)
├── models/          # modele DB: Casino, Bonus, Category, BlogPost (krok 2)
├── routers/         # endpointy: home, casino, bonusy, top, blog (krok 5+)
├── templates/       # szablony Jinja2
│   ├── base.html    # + canonical / hreflang / Open Graph
│   ├── partials/    # header (przełącznik języków), footer (disclaimer 18+)
│   └── index.html
└── static/          # css / js / img
```

## Języki (i18n)

Serwis jest dwujęzyczny: **ukraiński (domyślny) + rosyjski**, z przełącznikiem.
Każdy język ma własny prefiks w URL (lepsze SEO + tagi `hreflang`):

```
/            -> przekierowanie na /uk/
/uk/...      -> wersja ukraińska
/ru/...      -> wersja rosyjska
```

## Uruchomienie (dev)

```powershell
# 1. Wirtualne środowisko
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Zależności
pip install -r requirements.txt

# 3. Konfiguracja
Copy-Item .env.example .env   # i uzupełnij DATABASE_URL

# 4. Start serwera
uvicorn app.main:app --reload
```

Strona: http://localhost:8000/ • Health: http://localhost:8000/health

## Style (Tailwind CSS — statyczny build, bez JS)

Strony serwujemy jako czysty HTML + statyczny CSS (bez Tailwind CDN / JavaScriptu),
co przyspiesza ładowanie i indeksację przez wyszukiwarki.

CSS budujemy **standalone CLI Tailwind** (nie wymaga Node.js):

```powershell
# 1. Pobierz CLI raz (binarka NIE jest w repo — patrz .gitignore)
New-Item -ItemType Directory -Force tools | Out-Null
Invoke-WebRequest "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe" -OutFile "tools\tailwindcss.exe"

# 2. Zbuduj CSS (po KAZDEJ zmianie klas w szablonach!)
.\build_css.ps1            # jednorazowo
.\build_css.ps1 -Watch     # tryb obserwacji podczas developmentu
```

Wejście: `app/static/css/input.css` → wyjście: `app/static/css/tailwind.css` (commitowane).
**Uwaga:** dodanie nowej klasy Tailwind w szablonie wymaga przebudowy CSS, inaczej styl się nie pojawi.

## Baza danych (PostgreSQL)

Modele: `Casino`, `Bonus`, `Category`, `BlogPost` (app/models/). Treść dwujęzyczna
w kolumnach `_uk` / `_ru` w tej samej tabeli.

```powershell
# 1. Utwórz bazę (po instalacji PostgreSQL)
createdb -U postgres casino_review

# 2. Ustaw DATABASE_URL w .env (z własnym hasłem postgres)
#    postgresql+psycopg2://postgres:HASLO@localhost:5432/casino_review

# 3. Utwórz tabele
python -m app.init_db

# 4. (opcjonalnie) Załaduj przykładowe dane
python -m app.seed
```

## Następne kroki

1. [x] Szkielet projektu (foldery, pliki)
2. [x] Modele SQLAlchemy + PostgreSQL (schemat + skrypty init/seed)
3. [ ] Pełna integracja szablonów Jinja2
4. [ ] Layout HTML/CSS (header, footer, strona główna)
5. [ ] Pierwszy router — strona główna z listą kasyn
