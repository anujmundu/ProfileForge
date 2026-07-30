"""Exponential Backoff Retry Policy for GitHub API Requests.

Handles transient HTTP errors (500, 502, 503, 504, network timeouts) while
immediately aborting authentication failures (401, 403).
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

from typing import TypeVar

T = TypeVar("T")


class GitHubRetryPolicy:
    """Configurable exponential backoff retry executor."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0) -> None:
        self.max_retries: int = max_retries
        self.backoff_factor: float = backoff_factor
        self.total_retries: int = 0

    def calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay in seconds for a given attempt."""
        return float(self.backoff_factor ** (attempt - 1))

    def should_retry(self, status_code: int, attempt: int) -> bool:
        """Determine if an HTTP status code is retryable."""
        if attempt >= self.max_retries:
            return False

        # Never retry authentication or rate limit errors
        if status_code in (401, 403, 429):
            return False

        # Retry transient server errors
        return status_code in (500, 502, 503, 504)
