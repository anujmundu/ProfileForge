"""Language Statistics Collector.

Aggregates language usage bytes across collected repositories via GitHubClient.
"""

from profileforge.collectors.exceptions import LanguageCollectionError
from profileforge.collectors.models import LanguageCollection, RepositoryCollection
from profileforge.github import GitHubClient, GitHubError, GitHubLanguageStatsModel


class LanguageCollector:
    """Collector for language usage statistics across repositories."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect(
        self, username: str, repo_collection: RepositoryCollection
    ) -> LanguageCollection:
        """Collect and aggregate language byte statistics for a list of repositories.

        Args:
            username: Target GitHub username.
            repo_collection: RepositoryCollection containing repositories.

        Returns:
            Canonical LanguageCollection instance.

        Raises:
            LanguageCollectionError: If language data collection fails.
        """
        stats_list: list[GitHubLanguageStatsModel] = []

        for repo in repo_collection.repositories:
            # Skip fork repositories from language totals if desired or process non-forks
            if repo.fork:
                continue

            try:
                owner, _, repo_name = repo.full_name.partition("/")
                if not owner or not repo_name:
                    owner, repo_name = username, repo.name

                stats = self._client.get_repository_languages(owner, repo_name)
                stats_list.append(stats)
            except GitHubError:
                # Log or swallow individual repository language errors to allow partial collection
                continue
            except Exception as exc:
                raise LanguageCollectionError(
                    f"Failed to collect language statistics for repository '{repo.full_name}': {exc}"
                ) from exc

        return LanguageCollection.from_language_stats_list(
            username=username, stats_list=stats_list
        )
