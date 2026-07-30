"""Canonical Presentation Models.

Immutable, presentation-independent content models produced by Generators subsystem.
Exposes semantic content only with zero rendering/formatting instructions.
Governed by 09_RENDERING_SPECIFICATION.md and 04_DOMAIN_MODEL_SPECIFICATION.md.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProfileModel(BaseModel):
    """Semantic user profile presentation model."""

    model_config = ConfigDict(frozen=True)

    username: str
    display_name: str = ""
    headline: str = ""
    summary: str = ""
    location: str = ""
    company: str = ""
    avatar_url: str = ""
    profile_url: str = ""


class StatisticsModel(BaseModel):
    """Semantic portfolio statistics presentation model."""

    model_config = ConfigDict(frozen=True)

    total_repositories: int = 0
    total_stars: int = 0
    total_forks: int = 0
    dominant_language: str = ""
    language_percentages: dict[str, float] = Field(default_factory=dict)
    active_repositories_count: int = 0


class FeaturedProjectItem(BaseModel):
    """Featured repository project entry."""

    model_config = ConfigDict(frozen=True)

    name: str
    full_name: str
    description: str = ""
    stars: int = 0
    forks: int = 0
    language: str = ""
    topics: list[str] = Field(default_factory=list)
    score: float = 0.0
    html_url: str = ""


class FeaturedProjectsModel(BaseModel):
    """Collection of featured project presentation entries."""

    model_config = ConfigDict(frozen=True)

    projects: list[FeaturedProjectItem] = Field(default_factory=list)
    total_count: int = 0


class TechnologyGroup(BaseModel):
    """Grouped technology entries."""

    model_config = ConfigDict(frozen=True)

    category_name: str
    technologies: list[str] = Field(default_factory=list)


class TechnologyStackModel(BaseModel):
    """Grouped technology stack presentation model."""

    model_config = ConfigDict(frozen=True)

    groups: list[TechnologyGroup] = Field(default_factory=list)
    all_technologies: list[str] = Field(default_factory=list)


class TimelineEvent(BaseModel):
    """Structured timeline activity event."""

    model_config = ConfigDict(frozen=True)

    title: str
    description: str = ""
    timestamp: str = ""
    event_type: str = "general"


class TimelineModel(BaseModel):
    """Structured activity timeline presentation model."""

    model_config = ConfigDict(frozen=True)

    events: list[TimelineEvent] = Field(default_factory=list)


class AchievementItem(BaseModel):
    """Structured portfolio achievement entry."""

    model_config = ConfigDict(frozen=True)

    identifier: str
    title: str
    description: str = ""
    evidence: str = ""
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    priority: int = Field(default=1, ge=1)


class AchievementsModel(BaseModel):
    """Collection of structured achievements."""

    model_config = ConfigDict(frozen=True)

    achievements: list[AchievementItem] = Field(default_factory=list)


class SectionModel(BaseModel):
    """Generic section container for composable presentation models."""

    model_config = ConfigDict(frozen=True)

    section_id: str
    title: str
    section_type: str
    content: dict[str, Any] = Field(default_factory=dict)


class PresentationModel(BaseModel):
    """Root immutable presentation model consumed by downstream Renderers."""

    model_config = ConfigDict(frozen=True)

    username: str
    profile: ProfileModel
    statistics: StatisticsModel
    featured_projects: FeaturedProjectsModel
    technology_stack: TechnologyStackModel
    timeline: TimelineModel
    achievements: AchievementsModel
    sections: list[SectionModel] = Field(default_factory=list)
    generated_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
