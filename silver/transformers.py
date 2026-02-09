"""
Silver Layer Transformers - Bronze to Silver ETL
Agent 2: Data Engineer
"""
from typing import Any, Dict, List

import polars as pl

from core.logging import logger


class GitHubTransformer:
    """Transform raw GitHub data from Bronze to Silver layer."""

    @staticmethod
    def transform_pull_request(raw_data: Dict[str, Any], bronze_id: str) -> Dict[str, Any]:
        """Transform raw PR data to structured format."""
        payload = raw_data.get("payload", {})
        pr = payload.get("pull_request", payload)

        return {
            "bronze_id": bronze_id,
            "repo_name": payload.get("repository", {}).get("full_name", "unknown"),
            "pr_number": pr.get("number"),
            "title": pr.get("title"),
            "author": pr.get("user", {}).get("login"),
            "state": pr.get("state"),
            "created_at_source": pr.get("created_at"),
            "merged_at": pr.get("merged_at"),
            "closed_at": pr.get("closed_at"),
            "additions": pr.get("additions", 0),
            "deletions": pr.get("deletions", 0),
            "changed_files": pr.get("changed_files", 0),
        }

    @staticmethod
    def transform_commit(raw_data: Dict[str, Any], bronze_id: str) -> Dict[str, Any]:
        """Transform raw commit data to structured format."""
        payload = raw_data.get("payload", {})
        commits = payload.get("commits", [])

        results = []
        for commit in commits:
            results.append({
                "bronze_id": bronze_id,
                "repo_name": payload.get("repository", {}).get("full_name", "unknown"),
                "sha": commit.get("id") or commit.get("sha"),
                "author": commit.get("author", {}).get("name"),
                "message": commit.get("message"),
                "committed_at": commit.get("timestamp"),
            })
        return results

    @staticmethod
    def batch_transform_with_polars(raw_records: List[Dict]) -> pl.DataFrame:
        """Use Polars for high-performance batch transformation."""
        df = pl.DataFrame(raw_records)

        # Extract nested JSON fields using Polars
        transformed = df.with_columns([
            pl.col("payload").struct.field("repository").struct.field("full_name").alias("repo_name"),
            pl.col("payload").struct.field("pull_request").struct.field("number").alias("pr_number"),
            pl.col("payload").struct.field("pull_request").struct.field("title").alias("title"),
        ])

        logger.info(f"Transformed {len(transformed)} records with Polars")
        return transformed


class JiraTransformer:
    """Transform raw Jira data from Bronze to Silver layer."""

    @staticmethod
    def transform_issue(raw_data: Dict[str, Any], bronze_id: str) -> Dict[str, Any]:
        """Transform raw Jira issue to structured format."""
        payload = raw_data.get("payload", {})
        fields = payload.get("fields", {})

        return {
            "bronze_id": bronze_id,
            "issue_key": payload.get("key"),
            "project_key": fields.get("project", {}).get("key"),
            "issue_type": fields.get("issuetype", {}).get("name"),
            "status": fields.get("status", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
            "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
            "created_at_source": fields.get("created"),
            "updated_at_source": fields.get("updated"),
            "resolved_at": fields.get("resolutiondate"),
            "story_points": fields.get("customfield_10016"),  # Common story points field
        }
