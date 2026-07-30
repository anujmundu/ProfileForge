"""Portfolio Summary Analyzer.

Assembles structured portfolio overview metrics.
No natural-language generation. Structured data only.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.analytics.models import (
    FeaturedRepositories,
    LanguageAnalysis,
    PortfolioSummary,
    SkillAnalysis,
)
from profileforge.collectors.models import CollectionSnapshot


class PortfolioAnalyzer:
    """Analyzer for assembling high-level portfolio summary metrics."""

    def analyze(
        self,
        snapshot: CollectionSnapshot,
        featured: FeaturedRepositories,
        languages: LanguageAnalysis,
        skills: SkillAnalysis,
    ) -> PortfolioSummary:
        """Construct canonical PortfolioSummary from collected and analyzed data."""
        total_stars = sum(r.stargazers_count for r in snapshot.repositories.repositories)
        total_forks = sum(r.forks_count for r in snapshot.repositories.repositories)

        strongest = (
            featured.featured[0].repository.name if featured.featured else ""
        )

        return PortfolioSummary(
            total_public_repos=snapshot.repositories.total_count,
            total_stars=total_stars,
            total_forks=total_forks,
            primary_language=languages.dominant_language,
            top_skills=list(skills.primary_skills),
            strongest_repository=strongest,
        )
