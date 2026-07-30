"""Activity Timeline Presentation Generator.

Generates structured activity timeline model.
No natural-language formatting.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.generators.models import TimelineEvent, TimelineModel


class TimelineGenerator:
    """Generator for activity timeline presentation model."""

    def generate(self, analytics: AnalyticsSnapshot) -> TimelineModel:
        """Generate TimelineModel."""
        events: list[TimelineEvent] = []

        for ranked in analytics.repository_ranking.ranked_repositories[:5]:
            r = ranked.repository
            if r.pushed_at or r.updated_at:
                events.append(
                    TimelineEvent(
                        title=f"Updated repository {r.name}",
                        description=r.description or f"Repository in {r.language}",
                        timestamp=r.pushed_at or r.updated_at,
                        event_type="repository_update",
                    )
                )

        return TimelineModel(events=events)
