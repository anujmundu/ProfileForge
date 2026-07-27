class GitHubClientError(Exception):
    """Base exception for GitHub services."""


class GitHubAuthenticationError(GitHubClientError):
    """Raised when authentication fails."""


class GitHubRateLimitError(GitHubClientError):
    """Raised when the GitHub API rate limit is exceeded."""