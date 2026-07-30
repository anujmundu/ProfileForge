"""Integration tests for Rendering & Animation subsystems.

Validates rendering PresentationModels into Markdown, SVG (with SMIL animations), and JSON artifacts.
Governed by 09_RENDERING_SPECIFICATION.md and 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation import AnimationOrchestrator
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


def test_rendering_and_animation_integration() -> None:
    """Verify animation definitions integrate with rendering models."""
    anim_orchestrator = AnimationOrchestrator()
    anim_def = anim_orchestrator.create_card_entrance_animation("stats_card_target")

    assert anim_def.enabled is True
    assert 'attributeName="opacity"' in anim_def.smil_markup

    model = PresentationModel(
        username="octocat",
        profile=ProfileModel(username="octocat", display_name="The Octocat"),
        statistics=StatisticsModel(total_stars=50),
        featured_projects=FeaturedProjectsModel(),
        technology_stack=TechnologyStackModel(),
        timeline=TimelineModel(),
        achievements=AchievementsModel(),
    )

    renderer_orchestrator = RendererOrchestrator()
    artifacts = renderer_orchestrator.render_presentation_model(model)

    assert artifacts.markdown_artifact is not None
    assert artifacts.json_artifact is not None
    assert len(artifacts.svg_artifacts) == 2
