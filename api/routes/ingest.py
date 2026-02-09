from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict
from core.database import get_db
from bronze.models import RawData
from core.logging import logger

router = APIRouter()

@router.post("/ingest/{source}", status_code=201)
async def ingest_data(
    source: str,
    request: Request,
    payload: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest raw data from a source (e.g., 'github', 'jira').
    The payload is stored as-is in the bronze_raw_data table.
    """
    try:
        # Simple heuristic to determine event type (can be improved per source)
        event_type = request.headers.get("X-GitHub-Event") or payload.get("event") or "unknown"
        
        raw_data = RawData(
            source=source,
            event_type=event_type,
            payload=payload
        )
        db.add(raw_data)
        await db.commit()
        await db.refresh(raw_data)
        
        logger.info(f"Ingested data from {source} (id={raw_data.id})")
        return {"status": "success", "id": str(raw_data.id)}

    except Exception as e:
        logger.error(f"Error ingesting data from {source}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
