#!/usr/bin/env bash
# run_all.sh - Rulează serviciile CyberNova pe macOS/Linux
# Echivalent cu pașii:
#   cd honeypot/cybernova-honeypot
#   python3 -m venv .venv
#   source .venv/bin/activate
#   pip install Flask
#   pip install Flask request (redundant, ignorăm eșecul)
#   python -m pip install requests
#   node server.js &
#   cd ../..
#   python honeypot/cybernova-honeypot/app.py
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
HONEYPOT_DIR="$REPO_ROOT/honeypot/cybernova-honeypot"

info()  { printf "[run_all] %s\n" "$*"; }
warn()  { printf "[run_all] WARN: %s\n" "$*" 1>&2; }
error() { printf "[run_all] ERROR: %s\n" "$*" 1>&2; exit 1; }

[ -d "$HONEYPOT_DIR" ] || error "Nu găsesc $HONEYPOT_DIR"

cd "$HONEYPOT_DIR"

# Creează venv dacă lipsește
if [ ! -d .venv ]; then
  info "Creez venv (.venv)..."
  python3 -m venv .venv
fi

# Activează venv
# shellcheck disable=SC1091
source .venv/bin/activate || warn "Nu pot activa .venv"

# Instalare/actualizare dependențe Python din requirements.txt (include python-dotenv)
info "Instalez dependențele Python din requirements.txt..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Asigură dependențele Node (dotenv, express, node-fetch etc.) la rădăcina repo-ului
cd "$REPO_ROOT"
if [ ! -d node_modules ]; then
  info "Instalez dependențele Node (npm install) în rădăcina repo-ului..."
  npm install
fi
cd "$HONEYPOT_DIR"

# Pornește Node în background
info "Pornesc Node server.js în background..."
node server.js &
NODE_PID=$!
info "Node PID=$NODE_PID"

cleanup() {
  info "Cleanup..."
  if kill -0 "$NODE_PID" 2>/dev/null; then
    kill "$NODE_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# Revino la root și pornește Flask
cd "$REPO_ROOT"
info "Pornesc Flask app (app.py)..."
python honeypot/cybernova-honeypot/app.py
