"""
Dashboard view models.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RepositoryCard:
    """Repository information prepared for rendering."""

    name: str
    description: str | None
    language: str | None
    stars: int
    forks: int
    html_url: str


@dataclass(slots=True, frozen=True)
class DashboardView:
    """Complete dashboard prepared for rendering."""

    username: str
    name: str | None
    bio: str | None

    total_repositories: int
    total_stars: int
    total_forks: int

    repositories: list[RepositoryCard]
