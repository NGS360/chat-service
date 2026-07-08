"""
Thin async HTTP client for the NGS360 REST API.

The agent's tools use this to fetch real data. Every request carries the
caller's bearer token, so the REST API enforces authorization — this service
never touches the database.
"""

import httpx

from config import get_settings


class NGS360Client:
    def __init__(self, token: str) -> None:
        settings = get_settings()
        self._base = settings.NGS360_API_URL.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}"}

    async def _get(self, path: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self._base}{path}", headers=self._headers)
            resp.raise_for_status()
            return resp.json()

    async def get_project(self, project_id: str) -> dict:
        # TODO: confirm the exact REST path/shape against the API's project router.
        return await self._get(f"/projects/{project_id}")
