#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_PID_FILE="$PROJECT_DIR/.pid/backend.pid"
FRONTEND_PID_FILE="$PROJECT_DIR/.pid/frontend.pid"

stop_process() {
  local name="$1"
  local pid_file="$2"

  if [ ! -f "$pid_file" ]; then
    echo "[$name] 실행 중이 아님"
    return
  fi

  local pid
  pid=$(cat "$pid_file")

  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null
    # 자식 프로세스도 정리
    pkill -P "$pid" 2>/dev/null
    echo "[$name] 종료 (PID: $pid)"
  else
    echo "[$name] 이미 종료됨"
  fi

  rm -f "$pid_file"
}

stop_process "프론트엔드" "$FRONTEND_PID_FILE"
stop_process "백엔드" "$BACKEND_PID_FILE"

echo ""
echo "황금배추 에이전트 종료 완료"
