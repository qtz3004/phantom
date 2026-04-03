import logging
import secrets
from datetime import datetime, timedelta, timezone

import httpx

from teams.auth import get_valid_token

logger = logging.getLogger("teams-hook")

GRAPH_API = "https://graph.microsoft.com/v1.0"


class SubscriptionManager:
    """Graph API 구독 생성/갱신/삭제 관리."""

    def __init__(self):
        self.subscription_id: str | None = None
        self.client_state: str = secrets.token_urlsafe(16)

    async def create(self, notification_url: str) -> dict:
        token = await get_valid_token()
        expiration = datetime.now(timezone.utc) + timedelta(minutes=60)

        payload = {
            "changeType": "created",
            "notificationUrl": notification_url,
            "resource": "/me/chats/getAllMessages",
            "expirationDateTime": expiration.isoformat(),
            "clientState": self.client_state,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{GRAPH_API}/subscriptions",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()
            self.subscription_id = data["id"]
            logger.info(f"[구독 생성] id={self.subscription_id}, 만료={expiration.isoformat()}")
            return data

    async def renew(self) -> dict:
        if not self.subscription_id:
            raise RuntimeError("활성 구독이 없습니다")

        token = await get_valid_token()
        expiration = datetime.now(timezone.utc) + timedelta(minutes=60)

        payload = {
            "expirationDateTime": expiration.isoformat(),
        }

        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{GRAPH_API}/subscriptions/{self.subscription_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            logger.info(f"[구독 갱신] id={self.subscription_id}, 만료={expiration.isoformat()}")
            return resp.json()

    async def delete(self):
        if not self.subscription_id:
            return

        token = await get_valid_token()
        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                f"{GRAPH_API}/subscriptions/{self.subscription_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            logger.info(f"[구독 삭제] id={self.subscription_id}")
            self.subscription_id = None


subscription_manager = SubscriptionManager()
