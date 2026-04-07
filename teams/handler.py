import logging
from datetime import datetime

import httpx

from teams.auth import get_valid_token

logger = logging.getLogger("teams-hook")

GRAPH_API = "https://graph.microsoft.com/v1.0"


_chat_name_cache: dict[str, str] = {}


async def _get_chat_name(client: httpx.AsyncClient, chat_id: str, token: str) -> str:
    """채팅방 이름을 조회한다. 1:1이면 상대방 이름, 그룹이면 topic을 반환."""
    if chat_id in _chat_name_cache:
        return _chat_name_cache[chat_id]

    resp = await client.get(
        f"{GRAPH_API}/me/chats/{chat_id}?$expand=members",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code != 200:
        return chat_id

    chat = resp.json()
    chat_type = chat.get("chatType", "")
    topic = chat.get("topic") or ""

    if topic:
        name = topic
    elif chat_type == "oneOnOne":
        members = chat.get("members", [])
        other = [m.get("displayName", "") for m in members if m.get("displayName")]
        name = f"1:1 {', '.join(other)}" if other else chat_id
    elif chat_type == "group":
        members = chat.get("members", [])
        names = [m.get("displayName", "") for m in members if m.get("displayName")]
        name = f"그룹({', '.join(names)})" if names else chat_id
    else:
        name = chat_id

    _chat_name_cache[chat_id] = name
    return name


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
        chat_name = await _get_chat_name(client, chat_id, token)

        body = msg.get("body", {})
        content = body.get("content", "")
        content_type = body.get("contentType", "text")
        if content_type == "html":
            import re
            content = re.sub(r"<[^>]+>", "", content).strip()

    sender_str = f"{sender} ({sender_email})" if sender_email else sender
    logger.info(
        f"[Teams] {timestamp} | 채팅방: {chat_name} | "
        f"발신자: {sender_str} | 메시지: {content}"
    )
