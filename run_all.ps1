$ErrorActionPreference = 'Continue'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = $ScriptRoot
$HoneypotDir = Join-Path $RepoRoot 'honeypot/cybernova-honeypot'

Write-Host "[run_all] Repo root: $RepoRoot" -ForegroundColor Cyan
Write-Host "[run_all] Honeypot dir: $HoneypotDir" -ForegroundColor Cyan

if (-not (Test-Path $HoneypotDir)) {
  Write-Host "[run_all] ERROR: Nu găsesc $HoneypotDir" -ForegroundColor Red
  exit 1
}

Set-Location $HoneypotDir

py -3 -m venv .venv

$activate = Join-Path '.venv' 'Scripts/Activate.ps1'
if (Test-Path $activate) { . $activate } else { Write-Host "[run_all] WARN: Nu pot activa .venv (lipsește Scriptul de activare)." -ForegroundColor Yellow }

if (Test-Path (Join-Path $HoneypotDir 'requirements.txt')) {
  pip install -r requirements.txt
} else {
  Write-Host "[run_all] WARN: Nu găsesc requirements.txt — sar peste instalare dependențe" -ForegroundColor Yellow
}

Write-Host "[run_all] Pornesc Node server.js în background..." -ForegroundColor Green
$nodeProc = Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory $HoneypotDir -PassThru
Write-Host "[run_all] Node PID=$($nodeProc.Id)" -ForegroundColor DarkGray
Start-Sleep -Seconds 2

Set-Location $RepoRoot

Write-Host "[run_all] Pornesc Flask app (app.py)..." -ForegroundColor Green
python honeypot/cybernova-honeypot/app.py

if ($nodeProc) {
  Write-Host "[run_all] Oprire Node (PID=$($nodeProc.Id))..." -ForegroundColor DarkGray
  try { $nodeProc.CloseMainWindow() | Out-Null } catch {}
  try { $nodeProc.Kill() | Out-Null } catch {}
}

Write-Host "[run_all] Gata." -ForegroundColor Cyan
