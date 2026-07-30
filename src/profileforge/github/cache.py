"""In-Memory TTL Caching for GitHub Integration Subsystem.

Provides endpoint-aware caching with configurable expiration and manual invalidation.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    """Represents a cached response payload with expiration timestamp."""

    data: Any
    created_at: float
    ttl_seconds: float

    @property
    def is_expired(self) -> bool:
        """Check if entry has passed its TTL."""
        if self.ttl_seconds <= 0:
            return False
        return (time.time() - self.created_at) > self.ttl_seconds


class GitHubCache:
    """Lightweight in-memory cache for API response payloads."""

    def __init__(self, enabled: bool = True, ttl_seconds: float = 3600.0) -> None:
        self.enabled: bool = enabled
        self.ttl_seconds: float = ttl_seconds
        self._store: dict[str, CacheEntry] = {}
        self.hits: int = 0
        self.misses: int = 0

    def _make_key(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """Build deterministic cache key from endpoint and sorted query parameters."""
        if not params:
            return endpoint
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{endpoint}?{param_str}"

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any | None:
        """Retrieve payload from cache if enabled, present, and unexpired."""
        if not self.enabled:
            return None

        key = self._make_key(endpoint, params)
        entry = self._store.get(key)

        if entry is None:
            self.misses += 1
            return None

        if entry.is_expired:
            del self._store[key]
            self.misses += 1
            return None

        self.hits += 1
        return entry.data

    def set(self, endpoint: str, data: Any, params: dict[str, Any] | None = None) -> None:
        """Store payload in cache if enabled."""
        if not self.enabled:
            return

        key = self._make_key(endpoint, params)
        self._store[key] = CacheEntry(
            data=data,
            created_at=time.time(),
            ttl_seconds=self.ttl_seconds,
        )

    def clear(self) -> None:
        """Clear all cached entries."""
        self._store.clear()

    def invalidate(self, endpoint: str, params: dict[str, Any] | None = None) -> bool:
        """Remove a specific endpoint entry from cache. Returns True if removed."""
        key = self._make_key(endpoint, params)
        if key in self._store:
            del self._store[key]
            return True
        return False
