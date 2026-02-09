"""
Silver Layer Models - Structured Data Tables
Agent 2: Data Engineer
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base


class GitHubPullRequest(Base):
    """Cleaned and structured Pull Request data from GitHub."""
    __tablename__ = "silver_github_pull_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bronze_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Extracted fields
    repo_name = Column(String, nullable=False, index=True)
    pr_number = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    author = Column(String, nullable=True, index=True)
    state = Column(String, nullable=True)  # open, closed, merged
    
    # Timestamps
    created_at_source = Column(DateTime, nullable=True)
    merged_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Metrics
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    changed_files = Column(Integer, default=0)
    
    # ETL metadata
    processed_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))


class GitHubCommit(Base):
    """Cleaned and structured Commit data from GitHub."""
    __tablename__ = "silver_github_commits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bronze_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    repo_name = Column(String, nullable=False, index=True)
    sha = Column(String, nullable=False, unique=True)
    author = Column(String, nullable=True, index=True)
    message = Column(String, nullable=True)
    
    committed_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))


class JiraIssue(Base):
    """Cleaned and structured Issue data from Jira."""
    __tablename__ = "silver_jira_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bronze_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    issue_key = Column(String, nullable=False, unique=True)
    project_key = Column(String, nullable=False, index=True)
    issue_type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    assignee = Column(String, nullable=True, index=True)
    reporter = Column(String, nullable=True)
    
    created_at_source = Column(DateTime, nullable=True)
    updated_at_source = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    story_points = Column(Float, nullable=True)
    
    processed_at = Column(DateTime, default=datetime.utcnow, server_default=text("now()"))
