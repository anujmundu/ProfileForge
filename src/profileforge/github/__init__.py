"""GitHub Integration Subsystem.

API communication, authentication, response normalization, caching, rate limiting, and retries.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

from profileforge.github.authentication import GitHubAuthenticator
from profileforge.github.cache import GitHubCache
from profileforge.github.client import GitHubClient
from profileforge.github.diagnostics import GitHubDiagnostics
from profileforge.github.endpoints import GitHubEndpoints
from profileforge.github.exceptions import (
    AuthenticationError,
    GitHubError,
    PaginationError,
    RateLimitError,
    RequestError,
    RetryExhaustedError,
)
from profileforge.github.models import (
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
    RateLimitModel,
)
from profileforge.github.pagination import GitHubPagination
from profileforge.github.retry import GitHubRetryPolicy

__all__ = [
    "AuthenticationError",
    "GitHubAuthenticator",
    "GitHubCache",
    "GitHubClient",
    "GitHubDiagnostics",
    "GitHubEndpoints",
    "GitHubError",
    "GitHubLanguageStatsModel",
    "GitHubPagination",
    "GitHubRepositoryModel",
    "GitHubRetryPolicy",
    "GitHubUserModel",
    "PaginationError",
    "RateLimitError",
    "RequestError",
    "RateLimitModel",
    "RetryExhaustedError",
]
