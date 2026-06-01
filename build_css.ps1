# Buduje statyczny CSS (Tailwind) z app/static/css/input.css.
# Uruchom PO KAZDEJ zmianie klas Tailwind w szablonach, inaczej nowe style sie nie pojawia.
#
#   .\build_css.ps1           # jednorazowy build (zminifikowany)
#   .\build_css.ps1 -Watch    # tryb obserwacji (przebudowuje na biezaco)

param([switch]$Watch)

$cliArgs = @('-i', 'app/static/css/input.css', '-o', 'app/static/css/tailwind.css')
if ($Watch) { $cliArgs += '--watch' } else { $cliArgs += '--minify' }

& .\tools\tailwindcss.exe @cliArgs
