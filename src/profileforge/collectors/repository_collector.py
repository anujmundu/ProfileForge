"""Repository Metadata Collector.

Retrieves repository metadata via GitHubClient and produces canonical RepositoryCollection.
"""

from profileforge.collectors.exceptions import RepositoryCollectionError
from profileforge.collectors.models import Repository, RepositoryCollection
from profileforge.github import GitHubClient, GitHubError


class RepositoryCollector:
    """Collector for user repositories metadata."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect(
        self, username: str | None = None, auto_paginate: bool = True
    ) -> RepositoryCollection:
        """Collect repositories for a user.

        Args:
            username: Target GitHub username. If None, fetches authenticated user's repos.
            auto_paginate: Whether to fetch all pages.

        Returns:
            Canonical RepositoryCollection instance.

        Raises:
            RepositoryCollectionError: If repository collection fails.
        """
        try:
            if username:
                raw_repos = self._client.get_user_repositories(
                    username, auto_paginate=auto_paginate
                )
                target_user = username
            else:
                raw_repos = self._client.get_authenticated_user_repositories(
                    auto_paginate=auto_paginate
                )
                target_user = "authenticated_user"

            domain_repos = [Repository.from_github_model(r) for r in raw_repos]

            return RepositoryCollection(
                username=target_user,
                repositories=domain_repos,
                total_count=len(domain_repos),
            )
        except GitHubError as exc:
            target = username or "authenticated_user"
            raise RepositoryCollectionError(
                f"Failed to collect repositories for '{target}': {exc}"
            ) from exc
