#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/.logs"

case "${1:-all}" in
  backend|b)
    echo "── 백엔드 로그 ($LOG_DIR/backend.log) ──"
    tail -f "$LOG_DIR/backend.log"
    ;;
  frontend|f)
    echo "── 프론트엔드 로그 ($LOG_DIR/frontend.log) ──"
    tail -f "$LOG_DIR/frontend.log"
    ;;
  all|*)
    echo "── 백엔드 + 프론트엔드 로그 ──"
    tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
    ;;
esac
