"""
core/seed.py — Database seeding script for development.

Creates mock users, projects, milestones, repositories, escrows, and reputation data.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import (
    AgentName,
    AgentResult,
    ConsensusResult,
    Escrow,
    EscrowStatus,
    Evidence,
    Milestone,
    MilestoneStatus,
    Project,
    ProjectStatus,
    Repository,
    Reputation,
    User,
)


async def seed_database() -> None:
    """Insert development seed data."""
    async with AsyncSessionLocal() as session:
        # Check if users already exist to prevent duplicate seeding
        existing_users = await session.execute(select(User))
        if existing_users.scalars().first():
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding database...")

        # 1. Create Users (Client and Developer)
        client = User(
            github_id=1111111,
            github_username="aegis-client",
            github_email="client@aegis.dev",
            display_name="Alice (Client)",
            bio="A Web3 developer funding milestone-based software projects.",
        )
        developer = User(
            github_id=2222222,
            github_username="aegis-dev",
            github_email="developer@aegis.dev",
            display_name="Bob (Developer)",
            bio="Senior full stack engineer specializing in AI and distributed systems.",
        )
        session.add_all([client, developer])
        await session.flush()  # populate IDs

        # 2. Create Reputations
        client_rep = Reputation(
            user_id=client.id,
            overall_score=1.0,
            total_projects=1,
            tier="trusted",
        )
        dev_rep = Reputation(
            user_id=developer.id,
            overall_score=0.92,
            total_milestones=5,
            successful_milestones=4,
            failed_milestones=1,
            total_projects=1,
            current_streak=3,
            tier="verified",
        )
        session.add_all([client_rep, dev_rep])

        # 3. Create Project
        project = Project(
            title="Aegis AI Agent Platform",
            description="AI-powered trust protocol verifying milestone deliverables.",
            status=ProjectStatus.ACTIVE,
            client_id=client.id,
            developer_id=developer.id,
        )
        session.add(project)
        await session.flush()

        # 4. Create Repository
        repo = Repository(
            project_id=project.id,
            github_repo_id=987654321,
            full_name="aegis-dev/Aegis",
            owner="aegis-dev",
            name="Aegis",
            clone_url="https://github.com/aegis-dev/Aegis.git",
            default_branch="main",
            stars_count=42,
            forks_count=5,
            open_issues_count=2,
            last_synced_at=datetime.now(UTC),
        )
        session.add(repo)

        # 5. Create Milestones
        # Milestone 1: Approved & Paid
        m1 = Milestone(
            project_id=project.id,
            title="Phase 0: Project Setup & Architecture Design",
            description="Establish repo layout, Docker configurations, and base backend routers.",
            acceptance_criteria="FastAPI base router responds with OK. Next.js app starts without build errors.",
            order_index=0,
            payment_amount=1500.000000,
            payment_token="USDC",
            status=MilestoneStatus.APPROVED,
            submitted_at=datetime.now(UTC),
        )
        # Milestone 2: Submitted & Verifying
        m2 = Milestone(
            project_id=project.id,
            title="Phase 1: Database Setup and Core Models",
            description="Implement all database domain models and configure migrations.",
            acceptance_criteria="SQLAlchemy tables created for all Aegis entities. Seed script executes correctly.",
            order_index=1,
            payment_amount=2500.000000,
            payment_token="USDC",
            status=MilestoneStatus.VERIFYING,
            submitted_at=datetime.now(UTC),
        )
        # Milestone 3: Pending
        m3 = Milestone(
            project_id=project.id,
            title="Phase 2: Authentication flow",
            description="Integrate Github OAuth login with secure sessions.",
            acceptance_criteria="Github redirect handles valid callbacks. Session tokens generated successfully.",
            order_index=2,
            payment_amount=2000.000000,
            payment_token="USDC",
            status=MilestoneStatus.PENDING,
        )
        session.add_all([m1, m2, m3])
        await session.flush()

        # 6. Create Escrow records for milestones
        escrow1 = Escrow(
            milestone_id=m1.id,
            escrow_address="SolanaEscrowAddress111111111111111111111111",
            amount=1500.000000,
            status=EscrowStatus.RELEASED,
            tx_signature="5J2qB8z...signature...released",
            funded_at=datetime.now(UTC),
            released_at=datetime.now(UTC),
        )
        escrow2 = Escrow(
            milestone_id=m2.id,
            escrow_address="SolanaEscrowAddress222222222222222222222222",
            amount=2500.000000,
            status=EscrowStatus.FUNDED,
            tx_signature="3K1mH9y...signature...funded",
            funded_at=datetime.now(UTC),
        )
        escrow3 = Escrow(
            milestone_id=m3.id,
            amount=2000.000000,
            status=EscrowStatus.PENDING,
        )
        session.add_all([escrow1, escrow2, escrow3])

        # 7. Create Verification records for Milestone 1 (Historical run)
        evidence1 = Evidence(
            milestone_id=m1.id,
            evidence_found=True,
            commits_count=8,
            files_changed=14,
            lines_added=450,
            lines_removed=50,
            confidence=0.8500,
            raw_commits=[
                {"sha": "abc1", "commit": {"message": "feat: init framework"}}
            ],
        )
        session.add(evidence1)

        result_argus = AgentResult(
            milestone_id=m1.id,
            agent_name=AgentName.ARGUS,
            passed=True,
            score=0.8500,
            reasoning="Valid commits found indicating codebase scaffolding.",
        )
        result_themis = AgentResult(
            milestone_id=m1.id,
            agent_name=AgentName.THEMIS,
            passed=True,
            score=0.9000,
            reasoning="Commit scope aligns fully with initial setup deliverables.",
        )
        result_dike = AgentResult(
            milestone_id=m1.id,
            agent_name=AgentName.DIKE,
            passed=True,
            score=0.8000,
            reasoning="Proper folder structure and dockerfiles defined.",
        )
        session.add_all([result_argus, result_themis, result_dike])

        consensus = ConsensusResult(
            milestone_id=m1.id,
            argus_passed=True,
            themis_passed=True,
            dike_passed=True,
            chronos_on_time=True,
            argus_confidence=0.8500,
            themis_scope_match=0.9000,
            dike_quality_score=0.8000,
            approved=True,
            overall_score=0.8600,
            reasoning="All core checks passed with strong agent consensus.",
            payment_triggered=True,
        )
        session.add(consensus)

        await session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
