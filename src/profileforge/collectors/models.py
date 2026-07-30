"""Canonical Internal Collection Models.

Immutable domain models produced by Collectors subsystem for downstream Analytics.
Exposes no raw GitHub API objects.
Governed by 04_DOMAIN_MODEL_SPECIFICATION.md and 08_ANALYTICS_SPECIFICATION.md.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from profileforge.github.models import (
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)


class User(BaseModel):
    """Canonical user profile model."""

    model_config = ConfigDict(frozen=True)

    id: int
    login: str
    name: str = ""
    bio: str = ""
    company: str = ""
    location: str = ""
    avatar_url: str = ""
    html_url: str = ""
    public_repos: int = 0
    public_gists: int = 0
    followers: int = 0
    following: int = 0
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_github_model(cls, model: GitHubUserModel) -> "User":
        """Convert GitHubUserModel into canonical User domain object."""
        return cls(
            id=model.id,
            login=model.login,
            name=model.name,
            bio=model.bio,
            company=model.company,
            location=model.location,
            avatar_url=model.avatar_url,
            html_url=model.html_url,
            public_repos=model.public_repos,
            public_gists=model.public_gists,
            followers=model.followers,
            following=model.following,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class Repository(BaseModel):
    """Canonical repository domain model."""

    model_config = ConfigDict(frozen=True)

    id: int
    name: str
    full_name: str
    description: str = ""
    private: bool = False
    fork: bool = False
    html_url: str = ""
    stargazers_count: int = 0
    forks_count: int = 0
    watchers_count: int = 0
    open_issues_count: int = 0
    language: str = ""
    topics: list[str] = Field(default_factory=list)
    license_name: str = ""
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    default_branch: str = "main"

    @classmethod
    def from_github_model(cls, model: GitHubRepositoryModel) -> "Repository":
        """Convert GitHubRepositoryModel into canonical Repository domain object."""
        return cls(
            id=model.id,
            name=model.name,
            full_name=model.full_name,
            description=model.description,
            private=model.private,
            fork=model.fork,
            html_url=model.html_url,
            stargazers_count=model.stargazers_count,
            forks_count=model.forks_count,
            watchers_count=model.watchers_count,
            open_issues_count=model.open_issues_count,
            language=model.language,
            topics=list(model.topics),
            license_name=model.license_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
            pushed_at=model.pushed_at,
            default_branch=model.default_branch,
        )


class RepositoryCollection(BaseModel):
    """Collection of user repositories."""

    model_config = ConfigDict(frozen=True)

    username: str
    repositories: list[Repository] = Field(default_factory=list)
    total_count: int = 0


class LanguageCollection(BaseModel):
    """Aggregated language usage statistics across collected repositories."""

    model_config = ConfigDict(frozen=True)

    username: str
    language_bytes: dict[str, int] = Field(default_factory=dict)
    total_bytes: int = 0

    @classmethod
    def from_language_stats_list(
        cls, username: str, stats_list: list[GitHubLanguageStatsModel]
    ) -> "LanguageCollection":
        """Aggregate multiple repository language statistics into a single collection."""
        aggregated: dict[str, int] = {}
        for stats in stats_list:
            for lang, count in stats.languages.items():
                aggregated[lang] = aggregated.get(lang, 0) + count

        total = sum(aggregated.values())
        return cls(
            username=username,
            language_bytes=aggregated,
            total_bytes=total,
        )


class ContributionCollection(BaseModel):
    """Contribution activity statistics."""

    model_config = ConfigDict(frozen=True)

    username: str
    has_data: bool = False
    total_commit_contributions: int = 0
    total_issue_contributions: int = 0
    total_pull_request_contributions: int = 0
    total_repository_contributions: int = 0


class OrganizationCollection(BaseModel):
    """Organization membership collection."""

    model_config = ConfigDict(frozen=True)

    username: str
    organizations: list[dict[str, Any]] = Field(default_factory=list)
    total_count: int = 0


class CollectionSnapshot(BaseModel):
    """Complete immutable snapshot of all collected domain metrics for a GitHub user."""

    model_config = ConfigDict(frozen=True)

    username: str
    user: User
    repositories: RepositoryCollection
    languages: LanguageCollection
    contributions: ContributionCollection
    organizations: OrganizationCollection
    collected_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
