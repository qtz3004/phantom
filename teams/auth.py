import logging
import os
import secrets
import time
from urllib.parse import urlencode

import httpx

logger = logging.getLogger("teams-hook")

GRAPH_SCOPES = "Chat.Read User.Read offline_access"


def load_credentials() -> dict:
    tenant_id = os.environ.get("TEAMS_TENANT_ID", "common")
    return {
        "client_id": os.environ["TEAMS_CLIENT_ID"],
        "client_secret": os.environ["TEAMS_CLIENT_SECRET"],
        "tenant_id": tenant_id,
        "redirect_uri": os.environ.get("TEAMS_REDIRECT_URI", "http://localhost:8123/api/teams/auth/callback"),
        "auth_base": f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0",
    }


class TokenStore:
    """메모리 기반 OAuth 토큰 저장소."""

    def __init__(self):
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self.expires_at: float = 0
        self.state: str = secrets.token_urlsafe(16)

    @property
    def is_authenticated(self) -> bool:
        return self.access_token is not None

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.expires_at

    def update(self, token_response: dict):
        self.access_token = token_response["access_token"]
        self.refresh_token = token_response.get("refresh_token", self.refresh_token)
        expires_in = token_response.get("expires_in", 3600)
        self.expires_at = time.time() + expires_in
        logger.info(f"[토큰 갱신] 만료: {expires_in}초 후")


token_store = TokenStore()


def get_auth_url() -> str:
    creds = load_credentials()
    token_store.state = secrets.token_urlsafe(16)
    params = {
        "client_id": creds["client_id"],
        "response_type": "code",
        "redirect_uri": creds["redirect_uri"],
        "scope": GRAPH_SCOPES,
        "state": token_store.state,
    }
    return f"{creds['auth_base']}/authorize?{urlencode(params)}"


async def exchange_code(code: str) -> dict:
    creds = load_credentials()
    data = {
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "code": code,
        "redirect_uri": creds["redirect_uri"],
        "grant_type": "authorization_code",
        "scope": GRAPH_SCOPES,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{creds['auth_base']}/token", data=data)
        resp.raise_for_status()
        token_data = resp.json()
        token_store.update(token_data)
        return token_data


async def refresh_access_token() -> str:
    creds = load_credentials()
    data = {
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": token_store.refresh_token,
        "grant_type": "refresh_token",
        "scope": GRAPH_SCOPES,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{creds['auth_base']}/token", data=data)
        resp.raise_for_status()
        token_data = resp.json()
        token_store.update(token_data)
        return token_store.access_token


async def get_valid_token() -> str:
    if token_store.is_expired and token_store.refresh_token:
        return await refresh_access_token()
    return token_store.access_token
