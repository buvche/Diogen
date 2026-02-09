"""
GitHub API Connector
Agent 3: Integration Engineer
"""
from typing import Any, Dict, List, Optional

import httpx

from core.config import settings
from core.logging import logger


class GitHubClient:
    """Client for interacting with GitHub REST API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to GitHub API."""
        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()

    async def get_pull_requests(
        self, owner: str, repo: str, state: str = "all", per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch pull requests from a repository."""
        logger.info(f"Fetching PRs for {owner}/{repo}")
        endpoint = f"/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": per_page}
        return await self._request("GET", endpoint, params=params)

    async def get_commits(
        self, owner: str, repo: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch commits from a repository."""
        logger.info(f"Fetching commits for {owner}/{repo}")
        endpoint = f"/repos/{owner}/{repo}/commits"
        params = {"per_page": per_page}
        return await self._request("GET", endpoint, params=params)

    async def get_deployments(
        self, owner: str, repo: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch deployments from a repository."""
        logger.info(f"Fetching deployments for {owner}/{repo}")
        endpoint = f"/repos/{owner}/{repo}/deployments"
        params = {"per_page": per_page}
        return await self._request("GET", endpoint, params=params)

    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository metadata."""
        endpoint = f"/repos/{owner}/{repo}"
        return await self._request("GET", endpoint)
