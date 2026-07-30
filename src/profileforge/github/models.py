"""Normalized Internal Models for GitHub API Responses.

Converts raw GitHub REST API responses into immutable, strongly typed internal models.
No raw GitHub API JSON leaves this subsystem.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md and 04_DOMAIN_MODEL_SPECIFICATION.md.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RateLimitModel(BaseModel):
    """Normalized rate limit metadata model."""

    model_config = ConfigDict(frozen=True)

    limit: int = Field(default=60, ge=0)
    remaining: int = Field(default=60, ge=0)
    reset_timestamp: int = Field(default=0, ge=0)
    used: int = Field(default=0, ge=0)

    @classmethod
    def from_headers(cls, headers: dict[str, str]) -> "RateLimitModel":
        """Construct RateLimitModel from HTTP response headers."""
        limit = int(headers.get("x-ratelimit-limit", 60))
        remaining = int(headers.get("x-ratelimit-remaining", 60))
        reset_ts = int(headers.get("x-ratelimit-reset", 0))
        used = int(headers.get("x-ratelimit-used", max(0, limit - remaining)))

        return cls(
            limit=limit,
            remaining=remaining,
            reset_timestamp=reset_ts,
            used=used,
        )


class GitHubUserModel(BaseModel):
    """Normalized GitHub user profile model."""

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
    def from_api_response(cls, data: dict[str, Any]) -> "GitHubUserModel":
        """Normalize raw user API JSON dictionary into GitHubUserModel."""
        return cls(
            id=data.get("id", 0),
            login=data.get("login", ""),
            name=data.get("name") or "",
            bio=data.get("bio") or "",
            company=data.get("company") or "",
            location=data.get("location") or "",
            avatar_url=data.get("avatar_url") or "",
            html_url=data.get("html_url") or "",
            public_repos=data.get("public_repos", 0),
            public_gists=data.get("public_gists", 0),
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            created_at=data.get("created_at") or "",
            updated_at=data.get("updated_at") or "",
        )


class GitHubRepositoryModel(BaseModel):
    """Normalized GitHub repository metadata model."""

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
    def from_api_response(cls, data: dict[str, Any]) -> "GitHubRepositoryModel":
        """Normalize raw repository API JSON dictionary into GitHubRepositoryModel."""
        license_info = data.get("license")
        lic_name = ""
        if isinstance(license_info, dict):
            lic_name = license_info.get("name") or license_info.get("spdx_id") or ""

        return cls(
            id=data.get("id", 0),
            name=data.get("name", ""),
            full_name=data.get("full_name", ""),
            description=data.get("description") or "",
            private=data.get("private", False),
            fork=data.get("fork", False),
            html_url=data.get("html_url") or "",
            stargazers_count=data.get("stargazers_count", 0),
            forks_count=data.get("forks_count", 0),
            watchers_count=data.get("watchers_count", 0),
            open_issues_count=data.get("open_issues_count", 0),
            language=data.get("language") or "",
            topics=data.get("topics") or [],
            license_name=lic_name,
            created_at=data.get("created_at") or "",
            updated_at=data.get("updated_at") or "",
            pushed_at=data.get("pushed_at") or "",
            default_branch=data.get("default_branch") or "main",
        )


class GitHubLanguageStatsModel(BaseModel):
    """Normalized repository language statistics model."""

    model_config = ConfigDict(frozen=True)

    repository_name: str
    languages: dict[str, int] = Field(default_factory=dict)
    total_bytes: int = 0

    @classmethod
    def from_api_response(
        cls, repo_name: str, data: dict[str, int]
    ) -> "GitHubLanguageStatsModel":
        """Normalize raw language API JSON dictionary into GitHubLanguageStatsModel."""
        total = sum(data.values()) if data else 0
        return cls(
            repository_name=repo_name,
            languages=data,
            total_bytes=total,
        )
