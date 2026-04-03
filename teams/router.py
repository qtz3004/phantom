import asyncio
import logging

from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse

from teams.auth import exchange_code, get_auth_url, token_store
from teams.handler import fetch_and_log_message
from teams.subscription import subscription_manager

logger = logging.getLogger("teams-hook")

teams_router = APIRouter()

# 구독 갱신 백그라운드 태스크
_renew_task: asyncio.Task | None = None


async def _renew_loop():
    """50분마다 구독 갱신."""
    while True:
        await asyncio.sleep(50 * 60)
        try:
            await subscription_manager.renew()
        except Exception as e:
            logger.error(f"[구독 갱신 실패] {e}")


@teams_router.get("/auth")
async def auth():
    """Microsoft OAuth 로그인 페이지로 리디렉트."""
    url = get_auth_url()
    return RedirectResponse(url)


@teams_router.get("/auth/callback")
async def auth_callback(
    code: str = Query(...),
    state: str = Query(""),
):
    """OAuth 콜백. 토큰 교환 후 구독 생성."""
    global _renew_task

    if state != token_store.state:
        return {"error": "state 불일치"}

    await exchange_code(code)
    logger.info("[인증 완료] access_token 확보")

    # 구독 생성 — notification_url은 터널 URL 필요
    # 서버 시작 시 TEAMS_NOTIFICATION_URL 환경변수로 설정
    import os
    notification_url = os.environ.get("TEAMS_NOTIFICATION_URL")
    if not notification_url:
        return {
            "status": "authenticated",
            "warning": "TEAMS_NOTIFICATION_URL 환경변수가 설정되지 않아 구독을 생성하지 않았습니다. "
                       "환경변수 설정 후 서버를 재시작하세요.",
        }

    sub = await subscription_manager.create(notification_url)

    # 갱신 루프 시작
    if _renew_task is None or _renew_task.done():
        _renew_task = asyncio.create_task(_renew_loop())

    return {
        "status": "authenticated",
        "subscription_id": sub["id"],
    }


@teams_router.post("/notifications")
async def notifications(
    request: Request,
    validationToken: str = Query(None),
):
    """Graph API 웹훅 수신 엔드포인트."""
    # 1) 구독 검증
    if validationToken:
        logger.info("[구독 검증] validationToken 응답")
        return PlainTextResponse(content=validationToken, status_code=200)

    # 2) 알림 수신
    body = await request.json()
    notifications_list = body.get("value", [])

    for notification in notifications_list:
        # clientState 검증
        if notification.get("clientState") != subscription_manager.client_state:
            logger.warning("[알림 무시] clientState 불일치")
            continue

        resource = notification.get("resource", "")
        if resource:
            asyncio.create_task(fetch_and_log_message(resource))

    return PlainTextResponse(content="", status_code=202)
