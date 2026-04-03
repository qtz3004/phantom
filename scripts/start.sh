#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_PID_FILE="$PROJECT_DIR/.pid/backend.pid"
FRONTEND_PID_FILE="$PROJECT_DIR/.pid/frontend.pid"
LOG_DIR="$PROJECT_DIR/.logs"

mkdir -p "$PROJECT_DIR/.pid" "$LOG_DIR"

# 프로세스 살아있는지 확인
is_running() {
  [ -f "$1" ] && kill -0 "$(cat "$1")" 2>/dev/null
}

# 백엔드 시작
if is_running "$BACKEND_PID_FILE"; then
  echo "[백엔드] 이미 실행 중 (PID: $(cat "$BACKEND_PID_FILE"))"
else
  cd "$PROJECT_DIR"
  uv run python server.py > "$LOG_DIR/backend.log" 2>&1 &
  echo $! > "$BACKEND_PID_FILE"
  echo "[백엔드] 시작 (PID: $!, port: 8123)"
fi

# 프론트엔드 시작
if is_running "$FRONTEND_PID_FILE"; then
  echo "[프론트엔드] 이미 실행 중 (PID: $(cat "$FRONTEND_PID_FILE"))"
else
  cd "$PROJECT_DIR/frontend"
  npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
  echo $! > "$FRONTEND_PID_FILE"
  echo "[프론트엔드] 시작 (PID: $!, port: 3000)"
fi

echo ""
echo "황금배추 에이전트: http://localhost:3000"
echo "로그: $LOG_DIR/"

# 3초 후 브라우저 오픈
echo "3초 후 브라우저를 엽니다..."
sleep 3
open "http://localhost:3000"
