#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

case "${1:-all}" in
  backend|b)
    echo "── 백엔드 로그 ──"
    docker compose logs -f backend
    ;;
  frontend|f)
    echo "── 프론트엔드 로그 ──"
    docker compose logs -f frontend
    ;;
  all|*)
    echo "── 백엔드 + 프론트엔드 로그 ──"
    docker compose logs -f
    ;;
esac
