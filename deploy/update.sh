#!/usr/bin/env bash
# Оновлення сайту на сервері: підтягнути код -> оновити залежності -> рестарт.
# Викликається автоматично з GitHub Actions (.github/workflows/deploy.yml),
# або вручну на сервері:  bash /home/casino/site_revie/deploy/update.sh
set -euo pipefail

APP_DIR="/home/casino/site_revie"
cd "$APP_DIR"

echo "==> git pull"
git pull --ff-only origin main

echo "==> pip install (якщо змінилися залежності)"
"$APP_DIR/.venv/bin/pip" install -q -r requirements.txt

echo "==> restart сервісу"
sudo systemctl restart casino-review

echo "OK: задеплоєно $(date '+%Y-%m-%d %H:%M:%S')"
