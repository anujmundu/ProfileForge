"""Activity and Maintenance Recency Analyzer.

Analyzes update recency, maintenance indicators, and overall repository activity.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from datetime import UTC, datetime

from profileforge.analytics.models import ActivityAnalysis
from profileforge.collectors.models import CollectionSnapshot


class ActivityAnalyzer:
    """Analyzer for repository activity and update recency."""

    def analyze(self, snapshot: CollectionSnapshot) -> ActivityAnalysis:
        """Analyze repository activity indicators."""
        repos = snapshot.repositories.repositories
        if not repos:
            return ActivityAnalysis(
                active_repositories_count=0,
                recent_update_count=0,
                activity_level="INACTIVE",
                most_active_repository="",
            )

        now = datetime.now(UTC)
        recent_count = 0
        active_count = 0
        most_active_repo = repos[0].name if repos else ""
        max_stars = -1

        for repo in repos:
            ts_str = repo.pushed_at or repo.updated_at
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    days_old = (now - ts).days
                    if days_old <= 90:
                        recent_count += 1
                    if days_old <= 180:
                        active_count += 1
                except ValueError:
                    pass

            if repo.stargazers_count > max_stars:
                max_stars = repo.stargazers_count
                most_active_repo = repo.name

        total = len(repos)
        recent_ratio = recent_count / total if total > 0 else 0.0

        if recent_ratio >= 0.5:
            level = "HIGH"
        elif recent_ratio >= 0.2:
            level = "MODERATE"
        else:
            level = "LOW"

        return ActivityAnalysis(
            active_repositories_count=active_count,
            recent_update_count=recent_count,
            activity_level=level,
            most_active_repository=most_active_repo,
        )
