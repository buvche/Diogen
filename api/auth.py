"""
API Key Authentication Middleware
Agent 1: Backend Developer
"""
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from core.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify the API key from request headers.
    For development, if no API_KEY is configured, allow all requests.
    """
    if not settings.API_KEY:
        # Development mode: no authentication required
        return "dev-mode"

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")

    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return api_key
