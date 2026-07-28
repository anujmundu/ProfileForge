from datetime import datetime

from src.dashboard.builder import DashboardBuilder
from src.github.models import (
    DashboardData,
    DashboardStatistics,
    RepositorySummary,
    UserProfile,
)


def test_dashboard_builder():
    """Verify that DashboardBuilder transforms domain models into view models."""

    # Arrange
    profile = UserProfile(
        username="anujmundu",
        name="Anuj Mundu",
        bio="AI Engineer",
        avatar_url="https://example.com/avatar.png",
        followers=120,
        following=80,
        public_repositories=2,
    )

    repositories = [
        RepositorySummary(
            name="GitHubProfile",
            description="Profile Dashboard",
            language="Python",
            stars=20,
            forks=5,
            archived=False,
            fork=False,
            html_url="https://github.com/anujmundu/github-profile",
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 2, 1),
            pushed_at=datetime(2024, 2, 10),
            default_branch="main",
            visibility="public",
            size=500,
            topics=["python", "svg"],
            license_name="MIT",
        ),
        RepositorySummary(
            name="Portfolio",
            description="Personal Portfolio",
            language="TypeScript",
            stars=15,
            forks=2,
            archived=False,
            fork=False,
            html_url="https://github.com/anujmundu/portfolio",
            created_at=datetime(2023, 5, 1),
            updated_at=datetime(2023, 8, 1),
            pushed_at=datetime(2023, 8, 15),
            default_branch="main",
            visibility="public",
            size=300,
            topics=["react"],
            license_name=None,
        ),
    ]

    statistics = DashboardStatistics(
        total_repositories=2,
        total_stars=35,
        total_forks=7,
        archived_repositories=0,
        forked_repositories=0,
    )

    dashboard_data = DashboardData(
        profile=profile,
        repositories=repositories,
        statistics=statistics,
    )

    # Act
    builder = DashboardBuilder()
    dashboard = builder.build(dashboard_data)

    # Assert
    assert dashboard.username == profile.username
    assert dashboard.total_stars == statistics.total_stars
    assert len(dashboard.repositories) == len(repositories)
    assert dashboard.repositories[0].name == repositories[0].name
    assert dashboard.repositories[0].language == repositories[0].language
    assert dashboard.repositories[1].forks == repositories[1].forks