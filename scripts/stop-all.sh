#!/usr/bin/env bash
set -euo pipefail

echo "[backend] killing..."
pkill -f "python server.py" 2>/dev/null || true

echo "[frontend] killing..."
pkill -f "next-server|next dev|postcss.js" 2>/dev/null || true
lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true

sleep 1
echo "[done] remaining processes:"
ps aux | grep -E "next-server|next dev|postcss.js|python server.py" | grep -v grep || echo "  (none)"
