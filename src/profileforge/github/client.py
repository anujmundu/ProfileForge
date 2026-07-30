"""GitHub REST API Client.

Main client abstraction for communicating with GitHub REST API.
Single component permitted to execute HTTP requests to GitHub.
Normalizes all responses into canonical models.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

import time
from typing import Any, cast

import httpx

from profileforge.configuration import GitHubCategory, SecretStr
from profileforge.github.authentication import GitHubAuthenticator
from profileforge.github.cache import GitHubCache
from profileforge.github.diagnostics import GitHubDiagnostics
from profileforge.github.endpoints import GitHubEndpoints
from profileforge.github.exceptions import (
    AuthenticationError,
    RateLimitError,
    RequestError,
)
from profileforge.github.models import (
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
    RateLimitModel,
)
from profileforge.github.pagination import GitHubPagination
from profileforge.github.retry import GitHubRetryPolicy


class GitHubClient:
    """Production-grade GitHub REST API client using httpx with caching, retries, and normalization."""

    def __init__(
        self,
        config: GitHubCategory | None = None,
        auth_token: SecretStr | str | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._config = config or GitHubCategory()

        token = auth_token if auth_token is not None else self._config.auth_token
        self._authenticator = GitHubAuthenticator(token)

        self._base_url = str(self._config.api_endpoint).rstrip("/")
        self._timeout = self._config.timeout_seconds
        self._retry_policy = GitHubRetryPolicy(
            max_retries=self._config.max_retries,
            backoff_factor=self._config.backoff_factor,
        )
        self._cache = GitHubCache(
            enabled=self._config.cache_enabled,
            ttl_seconds=float(self._config.cache_ttl_seconds),
        )
        self._diagnostics = GitHubDiagnostics()

        headers = self._authenticator.get_headers()
        self._http_client = (
            http_client
            if http_client is not None
            else httpx.Client(
                base_url=self._base_url,
                headers=headers,
                timeout=self._timeout,
                follow_redirects=True,
            )
        )

    @property
    def authenticator(self) -> GitHubAuthenticator:
        """Get the authenticator instance."""
        return self._authenticator

    @property
    def diagnostics(self) -> GitHubDiagnostics:
        """Get the subsystem diagnostics instance."""
        return self._diagnostics

    @property
    def cache(self) -> GitHubCache:
        """Get the in-memory cache instance."""
        return self._cache

    def _execute_request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> tuple[Any, dict[str, str]]:
        """Execute HTTP GET request with caching, rate limiting, and retries.

        Returns:
            Tuple of (parsed_json_body, response_headers).
        """
        # 1. Cache lookup
        cached = self._cache.get(endpoint, params)
        if cached is not None:
            return cast(tuple[Any, dict[str, str]], cached)

        attempt = 0
        start_time = time.perf_counter()

        while True:
            attempt += 1
            try:
                response = self._http_client.get(endpoint, params=params)
                duration_ms = (time.perf_counter() - start_time) * 1000.0

                headers = dict(response.headers)
                rate_limit = RateLimitModel.from_headers(headers)
                self._diagnostics.update_rate_limit(rate_limit)

                # Check status codes
                if response.status_code == 401 or response.status_code == 403:
                    if rate_limit.remaining == 0:
                        raise RateLimitError("GitHub API rate limit exceeded.")
                    raise AuthenticationError(
                        f"GitHub authentication failed (HTTP {response.status_code}): {response.text}"
                    )

                if response.status_code == 429:
                    raise RateLimitError("GitHub API rate limit exceeded.")

                if response.status_code >= 400:
                    if self._retry_policy.should_retry(response.status_code, attempt):
                        self._diagnostics.record_retry()
                        time.sleep(self._retry_policy.calculate_delay(attempt))
                        continue
                    raise RequestError(
                        f"GitHub API request to '{endpoint}' failed with status {response.status_code}: {response.text}"
                    )

                # Success
                self._diagnostics.record_request(duration_ms=duration_ms, success=True)
                json_data = response.json()
                result = (json_data, headers)

                self._cache.set(endpoint, result, params)
                return result

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                duration_ms = (time.perf_counter() - start_time) * 1000.0
                self._diagnostics.record_request(duration_ms=duration_ms, success=False)

                if attempt < self._config.max_retries:
                    self._diagnostics.record_retry()
                    time.sleep(self._retry_policy.calculate_delay(attempt))
                    continue
                raise RequestError(
                    f"GitHub API request to '{endpoint}' failed after {attempt} retries: {exc}"
                ) from exc

    def get_authenticated_user(self) -> GitHubUserModel:
        """Fetch profile for the currently authenticated user."""
        endpoint = GitHubEndpoints.user()
        data, _ = self._execute_request(endpoint)
        return GitHubUserModel.from_api_response(data)

    def get_user_profile(self, username: str) -> GitHubUserModel:
        """Fetch public profile for a specific GitHub user."""
        endpoint = GitHubEndpoints.user_profile(username)
        data, _ = self._execute_request(endpoint)
        return GitHubUserModel.from_api_response(data)

    def get_user_repositories(
        self, username: str, per_page: int = 100, auto_paginate: bool = True
    ) -> list[GitHubRepositoryModel]:
        """Fetch public repositories for a specific user."""
        endpoint = GitHubEndpoints.user_repositories(username)
        return self._fetch_repositories(
            endpoint=endpoint, per_page=per_page, auto_paginate=auto_paginate
        )

    def get_authenticated_user_repositories(
        self, per_page: int = 100, auto_paginate: bool = True
    ) -> list[GitHubRepositoryModel]:
        """Fetch repositories for the authenticated user."""
        endpoint = GitHubEndpoints.authenticated_user_repositories()
        return self._fetch_repositories(
            endpoint=endpoint, per_page=per_page, auto_paginate=auto_paginate
        )

    def _fetch_repositories(
        self, endpoint: str, per_page: int, auto_paginate: bool
    ) -> list[GitHubRepositoryModel]:
        """Internal helper for fetching repository lists with pagination."""
        params: dict[str, Any] = {"per_page": min(per_page, 100), "page": 1}
        repos: list[GitHubRepositoryModel] = []

        while True:
            data, headers = self._execute_request(endpoint, params=params)
            if not isinstance(data, list):
                break

            for item in data:
                repos.append(GitHubRepositoryModel.from_api_response(item))

            if not auto_paginate:
                break

            meta = GitHubPagination.parse_link_header(headers.get("link"))
            if not meta.next_url:
                break

            params["page"] = params["page"] + 1

        return repos

    def get_repository(self, owner: str, repo: str) -> GitHubRepositoryModel:
        """Fetch metadata for a single repository."""
        endpoint = GitHubEndpoints.repository(owner, repo)
        data, _ = self._execute_request(endpoint)
        return GitHubRepositoryModel.from_api_response(data)

    def get_repository_languages(
        self, owner: str, repo: str
    ) -> GitHubLanguageStatsModel:
        """Fetch language byte distribution for a repository."""
        endpoint = GitHubEndpoints.repository_languages(owner, repo)
        data, _ = self._execute_request(endpoint)
        return GitHubLanguageStatsModel.from_api_response(
            repo_name=f"{owner}/{repo}", data=data
        )

    def get_rate_limit(self) -> RateLimitModel:
        """Fetch current rate limit status from GitHub API."""
        endpoint = GitHubEndpoints.rate_limit()
        data, headers = self._execute_request(endpoint)
        if "resources" in data and "core" in data["resources"]:
            core = data["resources"]["core"]
            return RateLimitModel(
                limit=core.get("limit", 60),
                remaining=core.get("remaining", 60),
                reset_timestamp=core.get("reset", 0),
                used=core.get("used", 0),
            )
        return RateLimitModel.from_headers(headers)

    def close(self) -> None:
        """Close the underlying HTTP client transport."""
        self._http_client.close()
