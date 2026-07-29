from datetime import datetime

from src.github.models import RepositorySummary
from src.github.statistics import StatisticsEngine


def test_statistics_engine():
    repositories = [
        RepositorySummary(
            name="repo1",
            description=None,
            language="Python",
            stars=10,
            forks=2,
            archived=False,
            fork=False,
            html_url="https://example.com/repo1",
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 2, 1),
            pushed_at=datetime(2024, 2, 10),
            default_branch="main",
            visibility="public",
            size=150,
            topics=["python"],
            license_name="MIT",
        ),
        RepositorySummary(
            name="repo2",
            description=None,
            language="TypeScript",
            stars=5,
            forks=1,
            archived=True,
            fork=True,
            html_url="https://example.com/repo2",
            created_at=datetime(2023, 5, 1),
            updated_at=datetime(2023, 8, 1),
            pushed_at=datetime(2023, 8, 15),
            default_branch="main",
            visibility="public",
            size=75,
            topics=["typescript"],
            license_name=None,
        ),
    ]

    engine = StatisticsEngine()

    stats = engine.compute(repositories)

    assert stats.total_repositories == 2
    assert stats.total_stars == 15
    assert stats.total_forks == 3
    assert stats.archived_repositories == 1
    assert stats.forked_repositories == 1
