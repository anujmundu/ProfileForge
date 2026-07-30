"""Sections Presentation Generator.

Composes individual presentation models into composable SectionModel objects.
"""

from profileforge.generators.models import (
    AchievementsModel,
    FeaturedProjectsModel,
    ProfileModel,
    SectionModel,
    StatisticsModel,
    TechnologyStackModel,
    TimelineModel,
)


class SectionsGenerator:
    """Generator for creating structured SectionModel list for downstream renderers."""

    def compose_sections(
        self,
        profile: ProfileModel,
        statistics: StatisticsModel,
        featured: FeaturedProjectsModel,
        tech_stack: TechnologyStackModel,
        timeline: TimelineModel,
        achievements: AchievementsModel,
    ) -> list[SectionModel]:
        """Compose presentation sub-models into structured SectionModel objects."""
        return [
            SectionModel(
                section_id="profile_header",
                title="Profile Header",
                section_type="profile",
                content=profile.model_dump(),
            ),
            SectionModel(
                section_id="portfolio_statistics",
                title="Portfolio Statistics",
                section_type="statistics",
                content=statistics.model_dump(),
            ),
            SectionModel(
                section_id="featured_projects",
                title="Featured Projects",
                section_type="featured",
                content=featured.model_dump(),
            ),
            SectionModel(
                section_id="technology_stack",
                title="Technology Stack",
                section_type="technology",
                content=tech_stack.model_dump(),
            ),
            SectionModel(
                section_id="activity_timeline",
                title="Activity Timeline",
                section_type="timeline",
                content=timeline.model_dump(),
            ),
            SectionModel(
                section_id="achievements",
                title="Achievements",
                section_type="achievements",
                content=achievements.model_dump(),
            ),
        ]
