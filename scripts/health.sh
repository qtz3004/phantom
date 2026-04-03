#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/.logs"
BACKEND_PID_FILE="$PROJECT_DIR/.pid/backend.pid"
FRONTEND_PID_FILE="$PROJECT_DIR/.pid/frontend.pid"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "=== 황금배추 에이전트 상태 점검 ==="
echo ""

# 1. 프로세스 상태
echo "── 프로세스 ──"
if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
  echo -e "  백엔드:    ${GREEN}실행 중${NC} (PID: $(cat "$BACKEND_PID_FILE"))"
else
  echo -e "  백엔드:    ${RED}중지됨${NC}"
fi

if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
  echo -e "  프론트엔드: ${GREEN}실행 중${NC} (PID: $(cat "$FRONTEND_PID_FILE"))"
else
  echo -e "  프론트엔드: ${RED}중지됨${NC}"
fi
echo ""

# 2. 엔드포인트 헬스체크
echo "── 엔드포인트 ──"
# AG-UI endpoint는 필수 필드 없이 호출하면 422를 반환 (정상 동작)
BACKEND_RESP=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8123/ -H "Content-Type: application/json" -d '{}' --max-time 3 2>/dev/null)
if [ "$BACKEND_RESP" = "422" ] || [ "$BACKEND_RESP" = "200" ]; then
  echo -e "  백엔드 API:  ${GREEN}OK${NC} (AG-UI endpoint, HTTP $BACKEND_RESP)"
else
  echo -e "  백엔드 API:  ${RED}FAIL${NC} (HTTP $BACKEND_RESP)"
fi

FRONTEND_RESP=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 --max-time 3 2>/dev/null)
if [ "$FRONTEND_RESP" = "200" ]; then
  echo -e "  프론트엔드:  ${GREEN}OK${NC} (http://localhost:3000)"
else
  echo -e "  프론트엔드:  ${RED}FAIL${NC} (HTTP $FRONTEND_RESP)"
fi
echo ""

# 3. 최근 에러 로그
echo "── 서버 로그 (최근 에러) ──"
echo "  경로: $LOG_DIR/backend.log"
BACKEND_ERRORS=$(grep -i -E "error|exception|traceback" "$LOG_DIR/backend.log" 2>/dev/null | tail -5)
if [ -n "$BACKEND_ERRORS" ]; then
  echo -e "  ${RED}$BACKEND_ERRORS${NC}"
else
  echo -e "  ${GREEN}에러 없음${NC}"
fi
echo ""

echo "── 클라이언트 로그 (최근 에러) ──"
echo "  경로: $LOG_DIR/frontend.log"
FRONTEND_ERRORS=$(grep -i -E "error|unhandled|fail" "$LOG_DIR/frontend.log" 2>/dev/null | tail -5)
if [ -n "$FRONTEND_ERRORS" ]; then
  echo -e "  ${YELLOW}$FRONTEND_ERRORS${NC}"
else
  echo -e "  ${GREEN}에러 없음${NC}"
fi
echo ""

# 4. 전체 로그 꼬리
echo "── 백엔드 로그 (최근 10줄) ──"
tail -10 "$LOG_DIR/backend.log" 2>/dev/null || echo "  로그 파일 없음"
echo ""
echo "── 프론트엔드 로그 (최근 10줄) ──"
tail -10 "$LOG_DIR/frontend.log" 2>/dev/null || echo "  로그 파일 없음"
