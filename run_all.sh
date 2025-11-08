#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
HONEYPOT_DIR="$REPO_ROOT/honeypot/cybernova-honeypot"

info()  { printf "[run_all] %s\n" "$*"; }
warn()  { printf "[run_all] WARN: %s\n" "$*" 1>&2; }
error() { printf "[run_all] ERROR: %s\n" "$*" 1>&2; exit 1; }

[ -d "$HONEYPOT_DIR" ] || error "Nu găsesc $HONEYPOT_DIR"

cd "$HONEYPOT_DIR"

if [ ! -d .venv ]; then
  info "Creez venv (.venv)..."
  python3 -m venv .venv
fi

source .venv/bin/activate || warn "Nu pot activa .venv"

info "Instalez dependențele Python din requirements.txt..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd "$REPO_ROOT"
if [ ! -d node_modules ]; then
  info "Instalez dependențele Node (npm install) în rădăcina repo-ului..."
  npm install
fi
cd "$HONEYPOT_DIR"

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

cd "$REPO_ROOT"
info "Pornesc Flask app (app.py)..."
python honeypot/cybernova-honeypot/app.py
