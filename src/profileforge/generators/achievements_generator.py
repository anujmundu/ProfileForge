"""Achievements Presentation Generator.

Generates structured achievements from analytics metadata.
No emojis. No formatting instructions.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.generators.models import AchievementItem, AchievementsModel


class AchievementsGenerator:
    """Generator for portfolio achievements presentation model."""

    def generate(self, analytics: AnalyticsSnapshot) -> AchievementsModel:
        """Generate AchievementsModel."""
        achievements: list[AchievementItem] = []
        summary = analytics.portfolio_summary
        langs = analytics.language_analysis

        # 1. Star milestone achievement
        if summary.total_stars >= 100:
            achievements.append(
                AchievementItem(
                    identifier="star_milestone_100",
                    title="Popular Open Source Projects",
                    description=f"Accumulated {summary.total_stars} stargazers across repositories.",
                    evidence=f"Total stars: {summary.total_stars}",
                    confidence=1.0,
                    priority=1,
                )
            )

        # 2. Polyglot achievement
        if langs.total_languages >= 3:
            achievements.append(
                AchievementItem(
                    identifier="polyglot_engineer",
                    title="Polyglot Engineer",
                    description=f"Active across {langs.total_languages} programming languages.",
                    evidence=f"Languages: {', '.join(langs.language_percentages.keys())}",
                    confidence=0.9,
                    priority=2,
                )
            )

        # 3. Active maintainer achievement
        if analytics.activity_analysis.active_repositories_count >= 2:
            achievements.append(
                AchievementItem(
                    identifier="active_maintainer",
                    title="Active Maintainer",
                    description="Maintains multiple actively updated repositories.",
                    evidence=f"Active repos: {analytics.activity_analysis.active_repositories_count}",
                    confidence=0.85,
                    priority=3,
                )
            )

        return AchievementsModel(achievements=achievements)
