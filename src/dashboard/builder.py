"""
Dashboard builder.
"""

from src.dashboard.models import DashboardView
from src.dashboard.models import RepositoryCard
from src.github.models import DashboardData


class DashboardBuilder:
    """Builds dashboard view models from domain models."""

    def build(self, data: DashboardData) -> DashboardView:

        cards = [
            RepositoryCard(
                name=repo.name,
                description=repo.description,
                language=repo.language,
                stars=repo.stars,
                forks=repo.forks,
                html_url=repo.html_url,
            )
            for repo in data.repositories
        ]

        return DashboardView(
            username=data.profile.username,
            name=data.profile.name,
            bio=data.profile.bio,
            total_repositories=data.statistics.total_repositories,
            total_stars=data.statistics.total_stars,
            total_forks=data.statistics.total_forks,
            repositories=cards,
        )