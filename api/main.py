from fastapi import FastAPI
from core.config import settings
from core.logging import setup_logging
from api.routes import ingest

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(ingest.router, prefix="/api", tags=["ingestion"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}
