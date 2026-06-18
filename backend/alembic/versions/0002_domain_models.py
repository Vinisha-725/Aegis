"""Phase 1: Create all domain model tables

Revision ID: 0002_domain_models
Revises: 0001_initial
Create Date: 2026-06-18

Creates:
  - users
  - projects
  - milestones
  - repositories
  - evidence
  - agent_results
  - consensus_results
  - reputations
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002_domain_models"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("github_id", sa.BigInteger(), nullable=False),
        sa.Column("github_username", sa.String(255), nullable=False),
        sa.Column("github_email", sa.String(255), nullable=True),
        sa.Column("github_avatar_url", sa.Text(), nullable=True),
        sa.Column("github_access_token", sa.Text(), nullable=True),
        sa.Column("display_name", sa.String(255), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_users_github_id", "users", ["github_id"], unique=True)
    op.create_index(
        "ix_users_github_username", "users", ["github_username"], unique=True
    )

    # ── projects ───────────────────────────────────────────────────────────────
    project_status = sa.Enum(
        "draft", "active", "paused", "completed", "cancelled", name="project_status"
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", project_status, nullable=False, server_default="draft"),
        sa.Column(
            "client_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_projects_client_id", "projects", ["client_id"])
    op.create_index("ix_projects_developer_id", "projects", ["developer_id"])

    # ── milestones ─────────────────────────────────────────────────────────────
    milestone_status = sa.Enum(
        "pending",
        "in_progress",
        "submitted",
        "verifying",
        "approved",
        "rejected",
        "disputed",
        name="milestone_status",
    )
    op.create_table(
        "milestones",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("acceptance_criteria", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("payment_amount", sa.Numeric(18, 6), nullable=True),
        sa.Column(
            "payment_token", sa.String(10), nullable=False, server_default="USDC"
        ),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", milestone_status, nullable=False, server_default="pending"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_milestones_project_id", "milestones", ["project_id"])
    op.create_index("ix_milestones_status", "milestones", ["status"])

    # ── repositories ───────────────────────────────────────────────────────────
    op.create_table(
        "repositories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("github_repo_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("full_name", sa.String(512), nullable=False),
        sa.Column("owner", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("clone_url", sa.Text(), nullable=False),
        sa.Column(
            "default_branch", sa.String(255), nullable=False, server_default="main"
        ),
        sa.Column("is_private", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("stars_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("forks_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "open_issues_count", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_repositories_project_id", "repositories", ["project_id"], unique=True
    )

    # ── evidence ───────────────────────────────────────────────────────────────
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "milestone_id",
            sa.String(36),
            sa.ForeignKey("milestones.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "evidence_found", sa.Boolean(), nullable=False, server_default="false"
        ),
        sa.Column("commits_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("files_changed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lines_added", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lines_removed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "pull_requests_merged", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("confidence", sa.Numeric(5, 4), nullable=False, server_default="0.0"),
        sa.Column("raw_commits", sa.JSON(), nullable=True),
        sa.Column("raw_pull_requests", sa.JSON(), nullable=True),
        sa.Column("raw_branches", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_evidence_milestone_id", "evidence", ["milestone_id"])

    # ── agent_results ──────────────────────────────────────────────────────────
    agent_name = sa.Enum(
        "argus", "themis", "dike", "chronos", "kratos", name="agent_name"
    )
    op.create_table(
        "agent_results",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "milestone_id",
            sa.String(36),
            sa.ForeignKey("milestones.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("agent_name", agent_name, nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("score", sa.Numeric(5, 4), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column("output", sa.JSON(), nullable=True),
        sa.Column("llm_model", sa.String(100), nullable=True),
        sa.Column("llm_tokens_used", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_agent_results_milestone_id", "agent_results", ["milestone_id"])
    op.create_index("ix_agent_results_agent_name", "agent_results", ["agent_name"])

    # ── consensus_results ─────────────────────────────────────────────────────
    op.create_table(
        "consensus_results",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "milestone_id",
            sa.String(36),
            sa.ForeignKey("milestones.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("argus_passed", sa.Boolean(), nullable=False),
        sa.Column("themis_passed", sa.Boolean(), nullable=False),
        sa.Column("dike_passed", sa.Boolean(), nullable=False),
        sa.Column("chronos_on_time", sa.Boolean(), nullable=False),
        sa.Column("argus_confidence", sa.Numeric(5, 4), nullable=True),
        sa.Column("themis_scope_match", sa.Numeric(5, 4), nullable=True),
        sa.Column("dike_quality_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("chronos_lateness_hours", sa.Numeric(10, 2), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=False),
        sa.Column("overall_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column(
            "payment_triggered", sa.Boolean(), nullable=False, server_default="false"
        ),
        sa.Column("agent_outputs_snapshot", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_consensus_results_milestone_id",
        "consensus_results",
        ["milestone_id"],
        unique=True,
    )

    # ── reputations ───────────────────────────────────────────────────────────
    op.create_table(
        "reputations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("overall_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_milestones", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "successful_milestones", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "failed_milestones", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "disputed_milestones", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("total_projects", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tier", sa.String(20), nullable=False, server_default="newcomer"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_reputations_user_id", "reputations", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_table("reputations")
    op.drop_table("consensus_results")
    op.drop_table("agent_results")
    op.drop_table("evidence")
    op.drop_table("repositories")
    op.drop_table("milestones")
    op.drop_table("projects")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS milestone_status")
    op.execute("DROP TYPE IF EXISTS project_status")
    op.execute("DROP TYPE IF EXISTS agent_name")
