"""
Jira API Connector
Agent 3: Integration Engineer
"""
from base64 import b64encode
from typing import Any, Dict, List, Optional

import httpx

from core.config import settings
from core.logging import logger


class JiraClient:
    """Client for interacting with Jira REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None
    ):
        self.base_url = (base_url or settings.JIRA_BASE_URL).rstrip("/")
        self.email = email or settings.JIRA_EMAIL
        self.api_token = api_token or settings.JIRA_API_TOKEN

        # Basic auth for Jira Cloud
        credentials = f"{self.email}:{self.api_token}"
        encoded = b64encode(credentials.encode()).decode()

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded}",
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to Jira API."""
        url = f"{self.base_url}/rest/api/3{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()

    async def get_issues(
        self,
        jql: str = "",
        fields: List[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """Search for issues using JQL."""
        logger.info(f"Fetching Jira issues with JQL: {jql}")
        endpoint = "/search"
        params = {
            "jql": jql,
            "maxResults": max_results,
        }
        if fields:
            params["fields"] = ",".join(fields)
        return await self._request("GET", endpoint, params=params)

    async def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get a single issue by key."""
        endpoint = f"/issue/{issue_key}"
        return await self._request("GET", endpoint)

    async def get_project(self, project_key: str) -> Dict[str, Any]:
        """Get project details."""
        endpoint = f"/project/{project_key}"
        return await self._request("GET", endpoint)

    async def get_sprints(self, board_id: int) -> Dict[str, Any]:
        """Get sprints for a board (requires Jira Software)."""
        # Note: This uses the Agile API
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
