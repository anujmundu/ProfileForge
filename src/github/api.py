"""
GitHub API client.
"""

import os

from dotenv import load_dotenv

from github import Auth, Github
from github.GithubException import (
    BadCredentialsException,
    GithubException,
    RateLimitExceededException,
)
from src.core.models import GitHubConfig
from src.github.exceptions import (
    GitHubAuthenticationError,
    GitHubClientError,
    GitHubRateLimitError,
)

load_dotenv()


class GitHubClient:
    """Low-level wrapper around the PyGithub client."""

    def __init__(self, config: GitHubConfig) -> None:
        token = os.getenv("GITHUB_TOKEN")

        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is not set.")

        auth = Auth.Token(token)

        self._client = Github(auth=auth)
        self._username = config.username

    def fetch_user(self):
        """Fetch the configured GitHub user."""

        try:
            return self._client.get_user(self._username)

        except BadCredentialsException as error:
            raise GitHubAuthenticationError("GitHub authentication failed.") from error

        except RateLimitExceededException as error:
            raise GitHubRateLimitError("GitHub API rate limit exceeded.") from error

        except GithubException as error:
            raise GitHubClientError(f"GitHub API error: {error}") from error

    def fetch_repositories(self):
        """Fetch the configured user's repositories."""

        try:
            return self.fetch_user().get_repos()

        except BadCredentialsException as error:
            raise GitHubAuthenticationError("GitHub authentication failed.") from error

        except RateLimitExceededException as error:
            raise GitHubRateLimitError("GitHub API rate limit exceeded.") from error

        except GithubException as error:
            raise GitHubClientError(f"GitHub API error: {error}") from error
