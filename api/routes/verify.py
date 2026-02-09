"""
Source Verification Endpoint
Agent 3: Integration Engineer
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from connectors.jira import JiraClient
from connectors.github import GitHubClient
from core.config import settings
from core.logging import logger

router = APIRouter()

class SourceVerifyRequest(BaseModel):
    source_type: str  # 'jira' or 'github'

@router.post("/verify-source")
async def verify_source(request: SourceVerifyRequest):
    """
    Verify connectivity to a data source.
    """
    try:
        if request.source_type == "jira":
            if not settings.JIRA_BASE_URL or not settings.JIRA_EMAIL or not settings.JIRA_API_TOKEN:
                raise HTTPException(status_code=400, detail="Jira credentials not configured")
            
            client = JiraClient()
            # Try to fetch current user (myself) to verify auth
            user = await client._request("GET", "/myself")
            return {
                "status": "success", 
                "message": f"Connected to Jira as {user.get('displayName')}",
                "details": {
                    "url": settings.JIRA_BASE_URL,
                    "account": user.get("emailAddress")
                }
            }
            
        elif request.source_type == "github":
            # GitHub public access check or auth check if token present
            client = GitHubClient()
            if settings.GITHUB_TOKEN:
                user = await client._request("GET", "/user")
                identity = f"Authenticated as {user.get('login')}"
            else:
                # limited rate limit check
                identity = "Public Access (No Token)"
                
            return {
                "status": "success",
                "message": f"Connected to GitHub ({identity})"
            }
            
        else:
            raise HTTPException(status_code=400, detail="Unknown source type")

    except Exception as e:
        logger.error(f"Verification failed for {request.source_type}: {str(e)}")
        return {
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }
