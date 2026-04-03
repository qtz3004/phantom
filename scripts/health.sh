#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "=== 황금배추 에이전트 상태 점검 ==="
echo ""

# 1. 컨테이너 상태
echo "── 컨테이너 ──"
docker compose ps
echo ""

# 2. 엔드포인트 헬스체크
echo "── 엔드포인트 ──"
BACKEND_RESP=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8123/health --max-time 3 2>/dev/null)
if [ "$BACKEND_RESP" = "200" ]; then
  echo -e "  백엔드 API:  ${GREEN}OK${NC} (http://localhost:8123)"
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

# 3. 최근 로그 에러
echo "── 백엔드 로그 (최근 에러) ──"
BACKEND_ERRORS=$(docker compose logs backend --tail=50 2>/dev/null | grep -i -E "error|exception|traceback" | tail -5)
if [ -n "$BACKEND_ERRORS" ]; then
  echo -e "  ${RED}$BACKEND_ERRORS${NC}"
else
  echo -e "  ${GREEN}에러 없음${NC}"
fi
echo ""

echo "── 백엔드 로그 (최근 10줄) ──"
docker compose logs backend --tail=10 2>/dev/null
echo ""
echo "── 프론트엔드 로그 (최근 10줄) ──"
docker compose logs frontend --tail=10 2>/dev/null
