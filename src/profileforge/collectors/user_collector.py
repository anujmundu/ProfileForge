"""User Profile Collector.

Retrieves user profile metadata via GitHubClient and produces canonical User model.
"""

from profileforge.collectors.exceptions import UserCollectionError
from profileforge.collectors.models import User
from profileforge.github import GitHubClient, GitHubError


class UserCollector:
    """Collector for GitHub user profile metadata."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def collect(self, username: str | None = None) -> User:
        """Collect user profile.

        Args:
            username: Target GitHub username. If None, fetches currently authenticated user.

        Returns:
            Canonical User domain model instance.

        Raises:
            UserCollectionError: If user profile retrieval fails.
        """
        try:
            if username:
                github_user = self._client.get_user_profile(username)
            else:
                github_user = self._client.get_authenticated_user()

            return User.from_github_model(github_user)
        except GitHubError as exc:
            target = username or "authenticated_user"
            raise UserCollectionError(
                f"Failed to collect user profile for '{target}': {exc}"
            ) from exc
