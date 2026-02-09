import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from core.database import Base


class RawData(Base):
    __tablename__ = "bronze_raw_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=True)
    payload = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))

    def __repr__(self):
        return f"<RawData(source='{self.source}', event_type='{self.event_type}', created_at='{self.created_at}')>"
