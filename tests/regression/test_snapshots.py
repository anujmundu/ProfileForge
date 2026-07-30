"""Snapshot regression tests for rendered artifact schemas.

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
from profileforge.renderers import JSONRenderer, MarkdownRenderer


def test_markdown_snapshot_structure() -> None:
    """Verify Markdown snapshot contains essential structural headers."""
    model = PresentationModel(
        username="octocat",
        profile=ProfileModel(username="octocat", display_name="The Octocat", headline="Craftsman"),
        statistics=StatisticsModel(total_repositories=5, total_stars=100, dominant_language="Python"),
        featured_projects=FeaturedProjectsModel(),
        technology_stack=TechnologyStackModel(),
        timeline=TimelineModel(),
        achievements=AchievementsModel(),
    )

    renderer = MarkdownRenderer()
    artifact = renderer.render(model)

    assert "# The Octocat" in artifact.content
    assert "Portfolio Overview" in artifact.content
    assert "Total Stars" in artifact.content


def test_json_snapshot_structure() -> None:
    """Verify JSON snapshot schema completeness."""
    model = PresentationModel(
        username="octocat",
        profile=ProfileModel(username="octocat"),
        statistics=StatisticsModel(),
        featured_projects=FeaturedProjectsModel(),
        technology_stack=TechnologyStackModel(),
        timeline=TimelineModel(),
        achievements=AchievementsModel(),
    )

    renderer = JSONRenderer()
    artifact = renderer.render(model)

    assert '"username": "octocat"' in artifact.json_content
    assert '"profile"' in artifact.json_content
    assert '"statistics"' in artifact.json_content
