"""
Gold Layer Models - Aggregated Metrics
Agent 2: Data Engineer
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, Date, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base


class DeploymentFrequency(Base):
    """DORA Metric: Deployment Frequency - how often deployments happen."""
    __tablename__ = "gold_deployment_frequency"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    repo_name = Column(String, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    deployment_count = Column(Integer, default=0)
    frequency_per_day = Column(Float, default=0.0)
    
    # Classification: Elite (multiple/day), High (daily-weekly), Medium (weekly-monthly), Low (monthly+)
    classification = Column(String, nullable=True)
    
    calculated_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))


class LeadTimeForChanges(Base):
    """DORA Metric: Lead Time for Changes - time from commit to production."""
    __tablename__ = "gold_lead_time"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    repo_name = Column(String, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    avg_lead_time_hours = Column(Float, default=0.0)
    median_lead_time_hours = Column(Float, default=0.0)
    p90_lead_time_hours = Column(Float, default=0.0)
    
    # Classification: Elite (<1hr), High (<1day), Medium (<1week), Low (>1week)
    classification = Column(String, nullable=True)
    
    calculated_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))


class ChangeFailureRate(Base):
    """DORA Metric: Change Failure Rate - percentage of failed deployments."""
    __tablename__ = "gold_change_failure_rate"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    repo_name = Column(String, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    total_deployments = Column(Integer, default=0)
    failed_deployments = Column(Integer, default=0)
    failure_rate_percent = Column(Float, default=0.0)
    
    # Classification: Elite (0-15%), High (16-30%), Medium (31-45%), Low (>45%)
    classification = Column(String, nullable=True)
    
    calculated_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))


class MeanTimeToRecovery(Base):
    """DORA Metric: MTTR - time to recover from failures."""
    __tablename__ = "gold_mttr"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    repo_name = Column(String, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    avg_recovery_time_hours = Column(Float, default=0.0)
    median_recovery_time_hours = Column(Float, default=0.0)
    incident_count = Column(Integer, default=0)
    
    # Classification: Elite (<1hr), High (<1day), Medium (<1week), Low (>1week)
    classification = Column(String, nullable=True)
    
    calculated_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))
