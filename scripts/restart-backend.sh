#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[backend] stopping..."
pkill -f "python server.py" 2>/dev/null || true
sleep 2

echo "[backend] starting..."
nohup uv run python server.py > /tmp/backend-stdout.log 2>&1 &
disown
sleep 4

if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q 200; then
  echo "[backend] OK  (http://localhost:8000)"
  echo "[backend] logs: $ROOT/logs/backend.log"
else
  echo "[backend] FAILED — tail /tmp/backend-stdout.log"
  tail -20 /tmp/backend-stdout.log
  exit 1
fi
