"""
GitHub data collectors.

Collectors transform PyGithub objects into the application's
domain models.
"""

import logging

from github.NamedUser import NamedUser
from github.Repository import Repository
from src.github.api import GitHubClient
from src.github.models import RepositorySummary, UserProfile

logger = logging.getLogger(__name__)


class GitHubCollector:
    """Collects GitHub data and converts it into domain models."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect_profile(self) -> UserProfile:
        """Collect the configured user's public profile."""

        user: NamedUser = self._client.fetch_user()

        return UserProfile(
            username=user.login,
            name=user.name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            followers=user.followers,
            following=user.following,
            public_repositories=user.public_repos,
        )

    def collect_repositories(self) -> list[RepositorySummary]:
        """Collect all public repositories."""

        repositories = self._client.fetch_repositories()

        summaries: list[RepositorySummary] = []

        for repo in repositories:
            summaries.append(self._build_repository_summary(repo))

        return summaries

    def _build_repository_summary(
        self,
        repo: Repository,
    ) -> RepositorySummary:
        """Convert a PyGithub repository into a RepositorySummary."""

        topics = self._safe_topics(repo)

        return RepositorySummary(
            name=repo.name,
            description=repo.description,
            language=repo.language,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            archived=repo.archived,
            fork=repo.fork,
            html_url=repo.html_url,
            created_at=repo.created_at,
            updated_at=repo.updated_at,
            pushed_at=repo.pushed_at,
            default_branch=repo.default_branch,
            visibility=repo.visibility,
            size=repo.size,
            topics=topics,
            license_name=(repo.license.name if repo.license is not None else None),
        )

    def _safe_topics(self, repo: Repository) -> list[str]:
        """Fetch repository topics without aborting collection."""

        try:
            return repo.get_topics()

        except Exception as error:
            logger.warning(
                "Failed to fetch topics for repository '%s': %s",
                repo.name,
                error,
            )
            return []
