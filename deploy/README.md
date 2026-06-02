# Деплой на VPS (UkrNames) — покроковий runbook

Піднімаємо наш сайт (FastAPI + PostgreSQL) на власному VPS і робимо авто-деплой:
`git push` локально → GitHub Actions сам оновлює сервер.

Усі конфіги вже готові в цій теці:
- `casino-review.service` — systemd-юніт (тримає застосунок живим)
- `nginx-casino-review.conf` — reverse proxy + статика
- `update.sh` — скрипт оновлення на сервері
- `../.github/workflows/deploy.yml` — авто-деплой з GitHub

> Приклади команд припускають: користувач **casino**, код у **/home/casino/site_revie**,
> Ubuntu 22.04/24.04 LTS. Якщо обереш інші імена — заміни їх у конфігах вище.

---

## ЕТАП 0 — Що замовити на UkrNames

1. **Домен** — реєструємо.
2. **VPS** — найменший тариф. При замовленні обери:
   - ОС: **Ubuntu 24.04 LTS** (або 22.04 LTS);
   - доступ: **root** по SSH (UkrNames пришле IP, логін `root` і пароль).

Після оплати ти отримаєш: **IP сервера**, **root-пароль**. Цього достатньо, щоб почати.

---

## ЕТАП 1 — Перший вхід і базова безпека

З локального PowerShell (заміни `IP` на свій):

```powershell
ssh root@IP
```

(введи root-пароль з листа UkrNames). Далі вже **на сервері**:

```bash
# оновити систему
apt update && apt upgrade -y

# створити робочого користувача 'casino' (без root для повсякдення)
adduser casino            # задай пароль, решту полів можна Enter
usermod -aG sudo casino   # дати право на sudo

# поставити все потрібне
apt install -y python3 python3-venv python3-pip git nginx postgresql postgresql-contrib
```

---

## ЕТАП 2 — База даних PostgreSQL

На сервері:

```bash
sudo -u postgres psql
```

У консолі psql (заміни `STRONGPASS` на свій надійний пароль):

```sql
CREATE USER casino WITH PASSWORD 'STRONGPASS';
CREATE DATABASE casino_review OWNER casino;
\q
```

---

## ЕТАП 3 — Код на сервері

> Спершу зроби ЕТАП «GitHub» з кореневого `../DEPLOY.md` (Крок 1–2): код має бути
> в приватному репозиторії на GitHub. Далі — клонуємо його на сервер.

Перемкнись на користувача casino і клонуй репозиторій:

```bash
su - casino
git clone https://github.com/Yura05/casino_review.git site_revie
cd site_revie

# віртуальне середовище + залежності
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

> CSS збирати на сервері НЕ треба: готовий `app/static/css/tailwind.css` уже в репозиторії.

---

## ЕТАП 4 — Налаштування (.env) і наповнення БД

Створи файл `.env` (НЕ комітиться, лежить лише на сервері):

```bash
nano /home/casino/site_revie/.env
```

Встав (підстав свій пароль БД і свій домен):

```
DATABASE_URL=postgresql+psycopg2://casino:STRONGPASS@localhost:5432/casino_review
SITE_NAME=Назва Сайту
SITE_URL=https://example.com
DEBUG=false
```

Створи таблиці й наповни демо-даними (один раз):

```bash
cd /home/casino/site_revie
.venv/bin/python -m app.init_db
.venv/bin/python -m app.seed
```

---

## ЕТАП 5 — Запуск під systemd

```bash
# скопіювати готовий юніт на місце
sudo cp /home/casino/site_revie/deploy/casino-review.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now casino-review     # запустити + автозапуск при ребуті
sudo systemctl status casino-review           # має бути 'active (running)'
```

Перевірка локально на сервері:

```bash
curl -s http://127.0.0.1:8000/health           # очікуємо {"status":"ok"}
```

---

## ЕТАП 6 — nginx + домен + HTTPS

```bash
# конфіг сайту
sudo cp /home/casino/site_revie/deploy/nginx-casino-review.conf /etc/nginx/sites-available/casino-review
# server_name уже містить casinorank.com.ua — додатково редагувати не треба

sudo ln -s /etc/nginx/sites-available/casino-review /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default          # прибрати дефолтну заглушку
sudo nginx -t && sudo systemctl reload nginx
```

**DNS:** у панелі UkrNames для домену вкажи `A`-запис на **IP сервера**
(і `A` для `www`, або `CNAME www -> домен`). Зачекай поширення (хвилини–години).

**HTTPS** (безкоштовний сертифікат, коли DNS уже вказує на сервер):

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d casinorank.com.ua -d www.casinorank.com.ua
```

Certbot сам допише SSL у nginx-конфіг і налаштує автопродовження.
✅ Сайт працює на `https://твій-домен`.

---

## ЕТАП 7 — Авто-деплой (git push → сайт оновлюється)

Щоб GitHub Actions міг заходити на сервер, створимо для нього SSH-ключ.

**На сервері** (від користувача casino):

```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/gh_deploy -N ""
cat ~/.ssh/gh_deploy.pub >> ~/.ssh/authorized_keys   # довіряємо цьому ключу вхід
chmod 600 ~/.ssh/authorized_keys
cat ~/.ssh/gh_deploy                                  # ПРИВАТНИЙ ключ — скопіюй увесь вивід
```

Дозволимо casino рестартувати сервіс без пароля (потрібно для update.sh):

```bash
echo "casino ALL=(ALL) NOPASSWD: /bin/systemctl restart casino-review" | sudo tee /etc/sudoers.d/casino-deploy
sudo chmod 440 /etc/sudoers.d/casino-deploy
```

**На GitHub** (репозиторій → Settings → Secrets and variables → Actions → New secret)
додай три секрети:

| Назва | Значення |
|-------|----------|
| `VPS_HOST` | IP сервера |
| `VPS_USER` | `casino` |
| `VPS_SSH_KEY` | весь приватний ключ (вивід `cat ~/.ssh/gh_deploy`, разом з рядками BEGIN/END) |

Готово. Тепер цикл такий:

```powershell
# локально, після правок через Claude Code:
.\deploy.ps1 "що змінив"
```

`deploy.ps1` збере CSS, закомітить і запушить → GitHub Actions зайде на сервер,
зробить `git pull` + `pip install` + рестарт. Сайт оновиться за ~1 хв.
Статус — у репозиторії, вкладка **Actions**.

---

## Якщо змінилася СТРУКТУРА БД

`git pull` оновлює лише код. Якщо додав нові колонки/таблиці в моделях —
зайди на сервер і застосуй зміни вручну:

```bash
cd /home/casino/site_revie
.venv/bin/python -m app.init_db        # створює нові таблиці (наявні не чіпає)
# для нових КОЛОНОК у наявних таблицях — окрема міграція, як app/migrate_*.py
```

## Корисні команди діагностики

```bash
sudo systemctl status casino-review        # стан застосунку
sudo journalctl -u casino-review -n 50      # останні логи застосунку
sudo nginx -t                               # перевірка конфігу nginx
sudo tail -n 50 /var/log/nginx/error.log    # логи nginx
```
