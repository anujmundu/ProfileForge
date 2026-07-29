"""
GitHub statistics engine.
"""

from src.github.models import DashboardStatistics, RepositorySummary


class StatisticsEngine:
    """Computes dashboard statistics from repository data."""

    def compute(
        self,
        repositories: list[RepositorySummary],
    ) -> DashboardStatistics:
        return DashboardStatistics(
            total_repositories=len(repositories),
            total_stars=sum(repo.stars for repo in repositories),
            total_forks=sum(repo.forks for repo in repositories),
            archived_repositories=sum(repo.archived for repo in repositories),
            forked_repositories=sum(repo.fork for repo in repositories),
        )
