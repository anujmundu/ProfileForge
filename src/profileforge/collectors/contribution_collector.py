"""Contribution Activity Collector.

Collects contribution statistics (or explicitly reports absence if unsupported by REST API).
"""

from profileforge.collectors.models import ContributionCollection
from profileforge.github import GitHubClient


class ContributionCollector:
    """Collector for user contribution activity statistics."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect(self, username: str) -> ContributionCollection:
        """Collect contribution activity metrics.

        Note: Standard GitHub REST API does not provide a single endpoint for complete
        contribution graph metrics without GraphQL. Exposes absence explicitly (`has_data=False`)
        rather than fabricating values.
        """
        return ContributionCollection(
            username=username,
            has_data=False,
            total_commit_contributions=0,
            total_issue_contributions=0,
            total_pull_request_contributions=0,
            total_repository_contributions=0,
        )
