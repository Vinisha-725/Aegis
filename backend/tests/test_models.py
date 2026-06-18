"""
tests/test_models.py — Unit tests verifying database model schemas and relationships.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.escrow import Escrow, EscrowStatus
from app.models.milestone import Milestone, MilestoneStatus
from app.models.project import Project, ProjectStatus
from app.models.repository import Repository
from app.models.reputation import Reputation
from app.models.user import User


def test_model_mappings_and_relationships() -> None:
    # Use in-memory SQLite to test table creation and mappings
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create client & developer users
    client = User(
        github_id=111,
        github_username="client_user",
        github_email="client@test.com",
    )
    developer = User(
        github_id=222,
        github_username="dev_user",
        github_email="dev@test.com",
    )
    session.add_all([client, developer])
    session.commit()

    # Verify primary keys generated
    assert client.id is not None
    assert developer.id is not None

    # Create reputations
    client_rep = Reputation(user_id=client.id, overall_score=1.0)
    dev_rep = Reputation(user_id=developer.id, overall_score=0.9)
    session.add_all([client_rep, dev_rep])
    session.commit()

    # Create project
    project = Project(
        title="Test Project",
        description="A project description",
        status=ProjectStatus.ACTIVE,
        client_id=client.id,
        developer_id=developer.id,
    )
    session.add(project)
    session.commit()

    # Create repository
    repo = Repository(
        project_id=project.id,
        github_repo_id=12345,
        full_name="owner/repo",
        owner="owner",
        name="repo",
        clone_url="https://github.com/owner/repo",
    )
    session.add(repo)
    session.commit()

    # Create milestones
    m1 = Milestone(
        project_id=project.id,
        title="Milestone 1",
        description="Desc 1",
        order_index=0,
        payment_amount=100.0,
        status=MilestoneStatus.PENDING,
    )
    session.add(m1)
    session.commit()

    # Create escrow
    escrow = Escrow(
        milestone_id=m1.id,
        escrow_address="SolanaAddress",
        amount=100.0,
        status=EscrowStatus.PENDING,
    )
    session.add(escrow)
    session.commit()

    # Verify relationships
    assert project.client.github_username == "client_user"
    assert project.developer.github_username == "dev_user"
    assert len(project.milestones) == 1
    assert project.milestones[0].title == "Milestone 1"
    assert project.repository.full_name == "owner/repo"

    assert m1.project.title == "Test Project"
    assert m1.escrow.escrow_address == "SolanaAddress"
    assert escrow.milestone.title == "Milestone 1"

    # Clean up
    session.close()
