"""Organization Membership Collector.

Collects public organization membership metadata via GitHubClient.
"""

from profileforge.collectors.exceptions import OrganizationCollectionError
from profileforge.collectors.models import OrganizationCollection
from profileforge.github import GitHubClient, GitHubError


class OrganizationCollector:
    """Collector for GitHub organization membership."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect(self, username: str) -> OrganizationCollection:
        """Collect organization membership for a user.

        Args:
            username: Target GitHub username.

        Returns:
            Canonical OrganizationCollection model.

        Raises:
            OrganizationCollectionError: If organization collection fails.
        """
        try:
            endpoint = f"/users/{username}/orgs"
            data, _ = self._client._execute_request(endpoint)
            orgs: list[dict[str, str]] = []

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        orgs.append(
                            {
                                "id": str(item.get("id", "")),
                                "login": str(item.get("login", "")),
                                "description": str(item.get("description") or ""),
                                "avatar_url": str(item.get("avatar_url") or ""),
                            }
                        )

            return OrganizationCollection(
                username=username,
                organizations=orgs,
                total_count=len(orgs),
            )
        except GitHubError as exc:
            raise OrganizationCollectionError(
                f"Failed to collect organization data for '{username}': {exc}"
            ) from exc
