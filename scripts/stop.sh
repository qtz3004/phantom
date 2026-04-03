#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=== 황금배추 에이전트 종료 ==="

docker compose down

echo ""
echo "황금배추 에이전트 종료 완료"
