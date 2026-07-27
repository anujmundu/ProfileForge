"""
Domain models used throughout the GitHub Profile Engine.

These models isolate the rest of the application from the PyGithub
implementation and represent the canonical data contracts used by the
dashboard and renderer.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserProfile:
    username: str
    name: str | None
    bio: str | None
    avatar_url: str
    followers: int
    following: int
    public_repositories: int


@dataclass(slots=True, frozen=True)
class RepositorySummary:
    name: str
    description: str | None
    language: str | None

    stars: int
    forks: int

    archived: bool
    fork: bool

    html_url: str
    
@dataclass(slots=True, frozen=True)
class DashboardStatistics:
    """Aggregated statistics used by the dashboard."""

    total_repositories: int
    total_stars: int
    total_forks: int
    archived_repositories: int
    forked_repositories: int
    
@dataclass(slots=True, frozen=True)
class DashboardData:
    """Complete dashboard data produced by the service layer."""

    profile: UserProfile
    repositories: list[RepositorySummary]
    statistics: DashboardStatistics