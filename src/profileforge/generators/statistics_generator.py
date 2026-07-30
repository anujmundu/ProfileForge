"""Statistics Presentation Generator.

Generates StatisticsModel from AnalyticsSnapshot.
Numeric and semantic statistics data only.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.generators.models import StatisticsModel


class StatisticsGenerator:
    """Generator for portfolio statistics presentation model."""

    def generate(self, analytics: AnalyticsSnapshot) -> StatisticsModel:
        """Generate StatisticsModel."""
        p_summary = analytics.portfolio_summary
        lang = analytics.language_analysis
        act = analytics.activity_analysis

        return StatisticsModel(
            total_repositories=p_summary.total_public_repos,
            total_stars=p_summary.total_stars,
            total_forks=p_summary.total_forks,
            dominant_language=lang.dominant_language,
            language_percentages=dict(lang.language_percentages),
            active_repositories_count=act.active_repositories_count,
        )
