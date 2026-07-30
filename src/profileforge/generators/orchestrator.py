"""Generator Orchestrator Implementation.

Coordinates modular generators in deterministic pipeline order to produce PresentationModel.
Governed by 09_RENDERING_SPECIFICATION.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import time

from profileforge.analytics import AnalyticsSnapshot
from profileforge.collectors import CollectionSnapshot
from profileforge.generators.achievements_generator import AchievementsGenerator
from profileforge.generators.diagnostics import GeneratorDiagnostics
from profileforge.generators.featured_generator import FeaturedGenerator
from profileforge.generators.models import PresentationModel
from profileforge.generators.profile_generator import ProfileGenerator
from profileforge.generators.sections_generator import SectionsGenerator
from profileforge.generators.statistics_generator import StatisticsGenerator
from profileforge.generators.technology_generator import TechnologyGenerator
from profileforge.generators.timeline_generator import TimelineGenerator


class GeneratorOrchestrator:
    """Single orchestration entry point for presentation model generation."""

    def __init__(self) -> None:
        self._profile_gen = ProfileGenerator()
        self._stats_gen = StatisticsGenerator()
        self._featured_gen = FeaturedGenerator()
        self._tech_gen = TechnologyGenerator()
        self._timeline_gen = TimelineGenerator()
        self._achievements_gen = AchievementsGenerator()
        self._sections_gen = SectionsGenerator()
        self._diagnostics = GeneratorDiagnostics()

    @property
    def diagnostics(self) -> GeneratorDiagnostics:
        """Get subsystem diagnostics tracker."""
        return self._diagnostics

    def generate_presentation_model(
        self, analytics: AnalyticsSnapshot, collection: CollectionSnapshot
    ) -> PresentationModel:
        """Execute deterministic generation pipeline to construct PresentationModel.

        Args:
            analytics: Canonical AnalyticsSnapshot produced by Analytics subsystem.
            collection: Canonical CollectionSnapshot produced by Collectors subsystem.

        Returns:
            Immutable PresentationModel consumed by Renderers.
        """
        start_time = time.perf_counter()

        profile = self._profile_gen.generate(analytics, collection)
        statistics = self._stats_gen.generate(analytics)
        featured = self._featured_gen.generate(analytics)
        tech_stack = self._tech_gen.generate(analytics)
        timeline = self._timeline_gen.generate(analytics)
        achievements = self._achievements_gen.generate(analytics)

        sections = self._sections_gen.compose_sections(
            profile=profile,
            statistics=statistics,
            featured=featured,
            tech_stack=tech_stack,
            timeline=timeline,
            achievements=achievements,
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        self._diagnostics.generation_duration_ms = duration_ms
        self._diagnostics.generated_sections_count = len(sections)

        return PresentationModel(
            username=analytics.username,
            profile=profile,
            statistics=statistics,
            featured_projects=featured,
            technology_stack=tech_stack,
            timeline=timeline,
            achievements=achievements,
            sections=sections,
        )
