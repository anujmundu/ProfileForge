"""GitHub Integration Diagnostics and Telemetry Collector.

Collects request metrics, cache utilization, retry counts, rate limit status, and failures.
Guarantees credentials are never exposed in diagnostics.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

from typing import Any

from profileforge.github.models import RateLimitModel


class GitHubDiagnostics:
    """Diagnostics collector for GitHub API requests and subsystem performance."""

    def __init__(self) -> None:
        self.request_count: int = 0
        self.retry_count: int = 0
        self.failed_request_count: int = 0
        self.total_response_time_ms: float = 0.0
        self.last_rate_limit: RateLimitModel | None = None

    def record_request(self, duration_ms: float, success: bool = True) -> None:
        """Record an API request duration and success status."""
        self.request_count += 1
        self.total_response_time_ms += duration_ms
        if not success:
            self.failed_request_count += 1

    def record_retry(self) -> None:
        """Record a retry attempt."""
        self.retry_count += 1

    def update_rate_limit(self, rate_limit: RateLimitModel) -> None:
        """Update recent rate limit status."""
        self.last_rate_limit = rate_limit

    def get_summary(
        self, cache_hits: int = 0, cache_misses: int = 0
    ) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        avg_time = (
            round(self.total_response_time_ms / self.request_count, 2)
            if self.request_count > 0
            else 0.0
        )
        return {
            "request_count": self.request_count,
            "failed_request_count": self.failed_request_count,
            "retry_count": self.retry_count,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "average_response_time_ms": avg_time,
            "rate_limit": (
                self.last_rate_limit.model_dump()
                if self.last_rate_limit
                else None
            ),
        }
