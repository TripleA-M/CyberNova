# run_all.ps1 - Rulează în ordine comenzile cerute și pornește ambele servicii
#
# Comenzile cerute (echivalente):
#   cd C:\Users\anton\Documents\GitHub\CyberNova\honeypot\cybernova-honeypot
#   py -3 -m venv .venv
#   .venv\Scripts\activate
#   pip install Flask
#   pip install Flask request
#   python -m pip install requests
#   node server.js
#   cd C:\Users\anton\Documents\GitHub\CyberNova
#   python honeypot/cybernova-honeypot/app.py
#
# Adaptări utile:
#  - Node pornește în background ca să poată porni și Flask din același script
#  - Căi calculate relativ la locația scriptului
#  - Nu oprim execuția dacă instalarea unui pachet e redundantă

$ErrorActionPreference = 'Continue'

# Localizează directoarele
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = $ScriptRoot
$HoneypotDir = Join-Path $RepoRoot 'honeypot/cybernova-honeypot'

Write-Host "[run_all] Repo root: $RepoRoot" -ForegroundColor Cyan
Write-Host "[run_all] Honeypot dir: $HoneypotDir" -ForegroundColor Cyan

if (-not (Test-Path $HoneypotDir)) {
  Write-Host "[run_all] ERROR: Nu găsesc $HoneypotDir" -ForegroundColor Red
  exit 1
}

# Echivalentul: cd .../honeypot/cybernova-honeypot
Set-Location $HoneypotDir

# Echivalentul: py -3 -m venv .venv
py -3 -m venv .venv

# Echivalentul: .venv\Scripts\activate
$activate = Join-Path '.venv' 'Scripts/Activate.ps1'
if (Test-Path $activate) { . $activate } else { Write-Host "[run_all] WARN: Nu pot activa .venv (lipsește Scriptul de activare)." -ForegroundColor Yellow }

# Instalează dependențele din requirements.txt
if (Test-Path (Join-Path $HoneypotDir 'requirements.txt')) {
  pip install -r requirements.txt
} else {
  Write-Host "[run_all] WARN: Nu găsesc requirements.txt — sar peste instalare dependențe" -ForegroundColor Yellow
}

# Echivalentul: node server.js (în background ca să putem continua)
Write-Host "[run_all] Pornesc Node server.js în background..." -ForegroundColor Green
$nodeProc = Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory $HoneypotDir -PassThru
Write-Host "[run_all] Node PID=$($nodeProc.Id)" -ForegroundColor DarkGray
Start-Sleep -Seconds 2

# Echivalentul: cd C:\Users\anton\Documents\GitHub\CyberNova
Set-Location $RepoRoot

# Echivalentul: python honeypot/cybernova-honeypot/app.py
Write-Host "[run_all] Pornesc Flask app (app.py)..." -ForegroundColor Green
python honeypot/cybernova-honeypot/app.py

# Cleanup: închide Node procesul pornit de acest script când Flask se oprește
if ($nodeProc) {
  Write-Host "[run_all] Oprire Node (PID=$($nodeProc.Id))..." -ForegroundColor DarkGray
  try { $nodeProc.CloseMainWindow() | Out-Null } catch {}
  try { $nodeProc.Kill() | Out-Null } catch {}
}

Write-Host "[run_all] Gata." -ForegroundColor Cyan
