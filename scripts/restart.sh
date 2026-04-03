#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=== 황금배추 에이전트 재시작 ==="
echo ""

docker compose down
docker compose up --build -d

echo ""
echo "황금배추 에이전트: http://localhost:3000"
