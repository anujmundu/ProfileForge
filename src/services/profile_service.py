"""
Profile service.

Coordinates GitHub data collection and statistics generation.
"""

from src.github.collectors import GitHubCollector
from src.github.statistics import StatisticsEngine


class ProfileService:
    """High-level service for building dashboard data."""

    def __init__(
        self,
        collector: GitHubCollector,
        statistics: StatisticsEngine,
    ) -> None:
        self._collector = collector
        self._statistics = statistics
        
    def build_dashboard(self):
        """Collect GitHub data and compute dashboard statistics."""

        profile = self._collector.collect_profile()

        repositories = self._collector.collect_repositories()

        stats = self._statistics.compute(repositories)

        return profile, repositories, stats
    
    