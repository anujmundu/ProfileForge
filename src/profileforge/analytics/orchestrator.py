"""Analytics Orchestrator Implementation.

Coordinates modular analyzers in deterministic pipeline order to assemble AnalyticsSnapshot.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 08_ANALYTICS_SPECIFICATION.md.
"""

import time

from profileforge.analytics.activity_analyzer import ActivityAnalyzer
from profileforge.analytics.diagnostics import AnalyticsDiagnostics
from profileforge.analytics.language_analyzer import LanguageAnalyzer
from profileforge.analytics.models import AnalyticsSnapshot
from profileforge.analytics.portfolio_analyzer import PortfolioAnalyzer
from profileforge.analytics.repository_analyzer import RepositoryAnalyzer
from profileforge.analytics.skill_analyzer import SkillAnalyzer
from profileforge.analytics.technology_analyzer import TechnologyAnalyzer
from profileforge.collectors.models import CollectionSnapshot
from profileforge.configuration import AnalyticsCategory


class AnalyticsOrchestrator:
    """Orchestrates deterministic analytics analysis pipeline."""

    def __init__(self, config: AnalyticsCategory | None = None) -> None:
        self._config = config or AnalyticsCategory()
        self._repo_analyzer = RepositoryAnalyzer(config=self._config)
        self._lang_analyzer = LanguageAnalyzer()
        self._tech_analyzer = TechnologyAnalyzer()
        self._skill_analyzer = SkillAnalyzer()
        self._activity_analyzer = ActivityAnalyzer()
        self._portfolio_analyzer = PortfolioAnalyzer()
        self._diagnostics = AnalyticsDiagnostics()

    @property
    def diagnostics(self) -> AnalyticsDiagnostics:
        """Get subsystem diagnostics collector."""
        return self._diagnostics

    def analyze_snapshot(self, snapshot: CollectionSnapshot) -> AnalyticsSnapshot:
        """Execute deterministic analytics pipeline on CollectionSnapshot.

        Args:
            snapshot: Canonical CollectionSnapshot produced by Collectors subsystem.

        Returns:
            Immutable AnalyticsSnapshot container.
        """
        start_time = time.perf_counter()

        # 1. Repository Scoring & Ranking
        ranking = self._repo_analyzer.analyze_ranking(snapshot.repositories)
        featured = self._repo_analyzer.select_featured(ranking)
        self._diagnostics.analyzed_repositories_count = ranking.total_count

        # 2. Language Analysis
        languages = self._lang_analyzer.analyze(snapshot.languages)

        # 3. Technology Inference
        technologies = self._tech_analyzer.analyze(snapshot)
        self._diagnostics.inferred_technologies_count = len(technologies.technologies)

        # 4. Skill Inference
        skills = self._skill_analyzer.analyze(snapshot, technologies)
        self._diagnostics.inferred_skills_count = len(skills.skills)

        # 5. Activity Analysis
        activity = self._activity_analyzer.analyze(snapshot)

        # 6. Portfolio Summary Assembly
        summary = self._portfolio_analyzer.analyze(
            snapshot=snapshot,
            featured=featured,
            languages=languages,
            skills=skills,
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        self._diagnostics.analysis_duration_ms = duration_ms

        return AnalyticsSnapshot(
            username=snapshot.username,
            repository_ranking=ranking,
            featured_repositories=featured,
            language_analysis=languages,
            technology_analysis=technologies,
            skill_analysis=skills,
            activity_analysis=activity,
            portfolio_summary=summary,
        )
