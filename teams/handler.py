import logging
from datetime import datetime

import httpx

from teams.auth import get_valid_token

logger = logging.getLogger("teams-hook")

GRAPH_API = "https://graph.microsoft.com/v1.0"


async def fetch_and_log_message(resource: str):
    """Graph API에서 메시지 본문을 조회하고 로깅한다."""
    token = await get_valid_token()

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GRAPH_API}/{resource}",
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code != 200:
            logger.warning(f"[메시지 조회 실패] {resp.status_code}: {resp.text}")
            return

        msg = resp.json()

    sender = "알 수 없음"
    sender_email = ""
    if "from" in msg and msg["from"]:
        user = msg["from"].get("user", {})
        sender = user.get("displayName", "알 수 없음")
        sender_email = user.get("userPrincipalName", "")

    created = msg.get("createdDateTime", "")
    try:
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        timestamp = created

    chat_id = msg.get("chatId", resource.split("/")[0] if "/" in resource else "")

    body = msg.get("body", {})
    content = body.get("content", "")
    content_type = body.get("contentType", "text")
    if content_type == "html":
        # HTML 태그 간단 제거
        import re
        content = re.sub(r"<[^>]+>", "", content).strip()

    if sender_email:
        logger.info(
            f"[Teams] {timestamp} | 채팅: {chat_id} | "
            f"발신자: {sender} ({sender_email}) | 메시지: {content}"
        )
    else:
        logger.info(
            f"[Teams] {timestamp} | 채팅: {chat_id} | "
            f"발신자: {sender} | 메시지: {content}"
        )
