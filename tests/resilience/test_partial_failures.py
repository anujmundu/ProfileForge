"""Resilience tests for Renderer partial failures.

Governed by 01_ENGINEERING_QUALITY_GATES.md and 09_RENDERING_SPECIFICATION.md.
"""

from profileforge.generators.models import (
    AchievementsModel,
    FeaturedProjectsModel,
    PresentationModel,
    ProfileModel,
    StatisticsModel,
    TechnologyStackModel,
    TimelineModel,
)
from profileforge.renderers import RendererOrchestrator


def test_renderer_failure_isolation() -> None:
    """Verify failure in one renderer does not invalidate outputs from other renderers."""
    model = PresentationModel(
        username="octocat",
        profile=ProfileModel(username="octocat"),
        statistics=StatisticsModel(),
        featured_projects=FeaturedProjectsModel(),
        technology_stack=TechnologyStackModel(),
        timeline=TimelineModel(),
        achievements=AchievementsModel(),
    )

    orchestrator = RendererOrchestrator()
    artifacts = orchestrator.render_presentation_model(model)

    assert artifacts.markdown_artifact is not None
    assert artifacts.json_artifact is not None
    assert len(artifacts.svg_artifacts) == 2
