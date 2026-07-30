"""GitHub Integration Subsystem Exception Hierarchy.

Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class GitHubError(ProfileForgeError):
    """Base exception for all GitHub integration subsystem errors."""


class AuthenticationError(GitHubError):
    """Raised when GitHub API authentication fails (e.g. invalid or expired token)."""


class RequestError(GitHubError):
    """Raised when an HTTP request fails or receives a non-200 response."""


class RateLimitError(GitHubError):
    """Raised when GitHub API rate limits are exceeded."""


class RetryExhaustedError(GitHubError):
    """Raised when transient retries are exhausted."""


class PaginationError(GitHubError):
    """Raised when GitHub pagination header parsing or iteration fails."""
