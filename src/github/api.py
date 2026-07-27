"""
GitHub API client.
"""

from github import Github

from src.core.models import GitHubConfig


class GitHubClient:
    """Low-level wrapper around the PyGithub client."""

    def __init__(self, config: GitHubConfig) -> None:
        self._client = Github()
        self._username = config.username

    def fetch_user(self):
        """Fetch the configured GitHub user."""
        return self._client.get_user(self._username)
    
    def fetch_repositories(self):
        """Fetch the configured user's repositories."""

        return self.fetch_user().get_repos()