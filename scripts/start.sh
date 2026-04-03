#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=== 황금배추 에이전트 시작 ==="

docker compose up --build -d

echo ""
echo "황금배추 에이전트: http://localhost:3000"
echo "백엔드 API:       http://localhost:8123"
echo ""

# 5초 후 브라우저 오픈
echo "5초 후 브라우저를 엽니다..."
sleep 5
open "http://localhost:3000"
