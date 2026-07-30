"""Canonical Internal Analytics Models.

Immutable analytics models produced by the Analytics subsystem for downstream Generators.
Governed by 04_DOMAIN_MODEL_SPECIFICATION.md and 08_ANALYTICS_SPECIFICATION.md.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from profileforge.collectors.models import Repository


class RepositoryScore(BaseModel):
    """Score breakdown for an individual repository."""

    model_config = ConfigDict(frozen=True)

    repository_name: str
    total_score: float = Field(ge=0.0, le=100.0)
    breakdown: dict[str, float] = Field(default_factory=dict)


class RankedRepository(BaseModel):
    """A repository paired with its deterministic score and rank."""

    model_config = ConfigDict(frozen=True)

    rank: int = Field(ge=1)
    repository: Repository
    score: RepositoryScore


class RepositoryRanking(BaseModel):
    """Ranked list of all user repositories."""

    model_config = ConfigDict(frozen=True)

    ranked_repositories: list[RankedRepository] = Field(default_factory=list)
    total_count: int = 0


class FeaturedRepositories(BaseModel):
    """Collection of top featured repositories selected by deterministic scoring."""

    model_config = ConfigDict(frozen=True)

    featured: list[RankedRepository] = Field(default_factory=list)
    count: int = 0


class LanguageAnalysis(BaseModel):
    """Analytical distribution of programming language usage."""

    model_config = ConfigDict(frozen=True)

    dominant_language: str = ""
    language_percentages: dict[str, float] = Field(default_factory=dict)
    total_languages: int = 0
    diversity_index: float = Field(default=0.0, ge=0.0, le=1.0)


class InferredTechnology(BaseModel):
    """Inferred technology stack entry."""

    model_config = ConfigDict(frozen=True)

    name: str
    category: str = "general"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source_repos: list[str] = Field(default_factory=list)


class TechnologyAnalysis(BaseModel):
    """Analytical summary of inferred technologies."""

    model_config = ConfigDict(frozen=True)

    technologies: list[InferredTechnology] = Field(default_factory=list)
    top_categories: list[str] = Field(default_factory=list)


class InferredSkill(BaseModel):
    """Inferred engineering skill entry with confidence and rationale."""

    model_config = ConfigDict(frozen=True)

    name: str
    category: str = "core"
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_repositories: list[str] = Field(default_factory=list)
    reason: str = ""


class SkillAnalysis(BaseModel):
    """Analytical summary of inferred engineering skills."""

    model_config = ConfigDict(frozen=True)

    skills: list[InferredSkill] = Field(default_factory=list)
    primary_skills: list[str] = Field(default_factory=list)


class ActivityAnalysis(BaseModel):
    """Analytical summary of repository maintenance and recency activity."""

    model_config = ConfigDict(frozen=True)

    active_repositories_count: int = 0
    recent_update_count: int = 0
    activity_level: str = "MODERATE"
    most_active_repository: str = ""


class PortfolioSummary(BaseModel):
    """High-level structured portfolio summary metrics."""

    model_config = ConfigDict(frozen=True)

    total_public_repos: int = 0
    total_stars: int = 0
    total_forks: int = 0
    primary_language: str = ""
    top_skills: list[str] = Field(default_factory=list)
    strongest_repository: str = ""


class AnalyticsSnapshot(BaseModel):
    """Complete immutable snapshot of all computed analytics models for a user."""

    model_config = ConfigDict(frozen=True)

    username: str
    repository_ranking: RepositoryRanking
    featured_repositories: FeaturedRepositories
    language_analysis: LanguageAnalysis
    technology_analysis: TechnologyAnalysis
    skill_analysis: SkillAnalysis
    activity_analysis: ActivityAnalysis
    portfolio_summary: PortfolioSummary
    analyzed_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
