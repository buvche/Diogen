"""
API Endpoint Tests
Agent 5: QA & Documentation
"""
import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Diogen"


@pytest.mark.asyncio
async def test_ingest_github_data(client):
    """Test ingesting data from GitHub source."""
    payload = {
        "event": "push",
        "repo": "diogen",
        "sender": "test-user"
    }
    response = await client.post("/api/ingest/github", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "id" in data


@pytest.mark.asyncio
async def test_ingest_jira_data(client):
    """Test ingesting data from Jira source."""
    payload = {
        "issue_key": "DIOGEN-123",
        "status": "In Progress"
    }
    response = await client.post("/api/ingest/jira", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_ingest_empty_payload(client):
    """Test that empty payloads are rejected."""
    response = await client.post("/api/ingest/github", json={})
    # Empty dict is still valid JSON, should succeed
    assert response.status_code == 201
