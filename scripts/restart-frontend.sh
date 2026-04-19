#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/frontend"

echo "[frontend] stopping..."
pkill -f "next-server|next dev|postcss.js" 2>/dev/null || true
lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 2

echo "[frontend] clearing cache..."
rm -rf .next node_modules/.cache

echo "[frontend] starting..."
nohup npm run dev > /dev/null 2>&1 &
disown
sleep 5

if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -qE "200|404|500"; then
  echo "[frontend] OK  (http://localhost:3000)"
  echo "[frontend] logs: $ROOT/logs/frontend.log"
else
  echo "[frontend] not responding yet — check $ROOT/logs/frontend.log"
  exit 1
fi

sleep 4
echo "[frontend] opening browser..."
open http://localhost:3000
