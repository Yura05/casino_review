# Деплой одним рухом: збирає CSS -> комітить -> пушить у GitHub.
# Render підхопить пуш і сам оновить сайт на домені (1-3 хв).
#
#   .\deploy.ps1 "опис що змінив"
#   .\deploy.ps1                 # опис згенерується автоматично (дата/час)
#
# Передумова: один раз налаштований git remote (origin) і гілка main
# (див. DEPLOY.md, Крок 1-2).

param([string]$Message)

$ErrorActionPreference = 'Stop'

if (-not $Message -or $Message.Trim() -eq '') {
    $Message = "Update site ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
}

Write-Host "==> 1/3 Збираю Tailwind CSS..." -ForegroundColor Cyan
& .\build_css.ps1
if ($LASTEXITCODE -ne 0) { Write-Host "Білд CSS впав — деплой зупинено." -ForegroundColor Red; exit 1 }

Write-Host "==> 2/3 Коміт змін..." -ForegroundColor Cyan
git add -A
# Якщо змін немає — git commit поверне ненульовий код; це не помилка деплою.
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host "Немає нових змін для коміту (або коміт не вдався). Пробую запушити поточний стан..." -ForegroundColor Yellow
}

Write-Host "==> 3/3 Пуш у GitHub (origin/main)..." -ForegroundColor Cyan
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Host "Push впав. Перевір git remote / автентифікацію." -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "Готово. Render зараз сам передеплоїть сайт (стеж на render.com -> Events)." -ForegroundColor Green
