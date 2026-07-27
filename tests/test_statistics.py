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
        ),
    ]

    engine = StatisticsEngine()

    stats = engine.compute(repositories)

    assert stats.total_repositories == 2
    assert stats.total_stars == 15
    assert stats.total_forks == 3
    assert stats.archived_repositories == 1
    assert stats.forked_repositories == 1