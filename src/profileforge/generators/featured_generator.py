"""Featured Projects Presentation Generator.

Generates FeaturedProjectsModel from AnalyticsSnapshot.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.generators.models import FeaturedProjectItem, FeaturedProjectsModel


class FeaturedGenerator:
    """Generator for featured projects presentation model."""

    def generate(self, analytics: AnalyticsSnapshot) -> FeaturedProjectsModel:
        """Generate FeaturedProjectsModel."""
        projects: list[FeaturedProjectItem] = []

        for ranked in analytics.featured_repositories.featured:
            r = ranked.repository
            projects.append(
                FeaturedProjectItem(
                    name=r.name,
                    full_name=r.full_name,
                    description=r.description,
                    stars=r.stargazers_count,
                    forks=r.forks_count,
                    language=r.language,
                    topics=list(r.topics),
                    score=ranked.score.total_score,
                    html_url=r.html_url,
                )
            )

        return FeaturedProjectsModel(
            projects=projects,
            total_count=len(projects),
        )
