"""Regression tests for pipeline determinism.

Governed by 01_ENGINEERING_QUALITY_GATES.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from profileforge.analytics import AnalyticsOrchestrator
from profileforge.collectors import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    Repository,
    RepositoryCollection,
    User,
)
from profileforge.generators import GeneratorOrchestrator


def test_analytics_and_generator_determinism() -> None:
    """Verify identical input snapshots produce identical AnalyticsSnapshot and PresentationModel."""
    user = User(id=1, login="octocat", name="Octocat")
    repo = Repository(id=101, name="r1", full_name="octocat/r1", stargazers_count=50)

    snapshot = CollectionSnapshot(
        username="octocat",
        user=user,
        repositories=RepositoryCollection(username="octocat", repositories=[repo], total_count=1),
        languages=LanguageCollection(username="octocat", language_bytes={"Python": 100}, total_bytes=100),
        contributions=ContributionCollection(username="octocat", has_data=False),
        organizations=OrganizationCollection(username="octocat", organizations=[], total_count=0),
    )

    analytics_orchestrator = AnalyticsOrchestrator()
    generator_orchestrator = GeneratorOrchestrator()

    a1 = analytics_orchestrator.analyze_snapshot(snapshot)
    a2 = analytics_orchestrator.analyze_snapshot(snapshot)
    assert a1.portfolio_summary == a2.portfolio_summary
    assert a1.language_analysis == a2.language_analysis

    p1 = generator_orchestrator.generate_presentation_model(a1, snapshot)
    p2 = generator_orchestrator.generate_presentation_model(a2, snapshot)
    assert p1.profile == p2.profile
    assert p1.statistics == p2.statistics
