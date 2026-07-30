"""Unit tests for GitHub Integration Subsystem using mocked HTTP responses.

All network calls are strictly mocked via httpx.MockTransport.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

from typing import Any

import httpx
import pytest

from profileforge.configuration import SecretStr
from profileforge.github import (
    AuthenticationError,
    GitHubAuthenticator,
    GitHubCache,
    GitHubClient,
    GitHubDiagnostics,
    GitHubLanguageStatsModel,
    GitHubPagination,
    GitHubRepositoryModel,
    GitHubUserModel,
    RateLimitError,
    RateLimitModel,
)


def create_mock_client(handler: Any) -> GitHubClient:
    """Helper to create a GitHubClient backed by an httpx.MockTransport."""
    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(
        base_url="https://api.github.com",
        transport=transport,
        follow_redirects=True,
    )
    return GitHubClient(http_client=http_client)


def test_authenticator_headers() -> None:
    """Verify headers generated in authenticated and anonymous modes."""
    auth_anon = GitHubAuthenticator()
    assert auth_anon.is_authenticated is False
    headers_anon = auth_anon.get_headers()
    assert "Authorization" not in headers_anon
    assert headers_anon["User-Agent"] == "ProfileForge-Engine"

    token = SecretStr("ghp_my_secret_token_1234567890")
    auth_pat = GitHubAuthenticator(auth_token=token)
    assert auth_pat.is_authenticated is True
    headers_pat = auth_pat.get_headers()
    assert headers_pat["Authorization"] == "Bearer ghp_my_secret_token_1234567890"

    # Redaction test
    assert "ghp_my_secret_token_1234567890" not in repr(auth_pat)
    assert "ghp_****" in repr(auth_pat)


def test_get_user_profile_normalization() -> None:
    """Verify fetching and normalizing a user profile response."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/users/octocat"
        return httpx.Response(
            200,
            json={
                "id": 583231,
                "login": "octocat",
                "name": "The Octocat",
                "bio": "GitHub mascot",
                "company": "@github",
                "location": "San Francisco",
                "public_repos": 8,
                "followers": 10000,
                "following": 9,
            },
            headers={"x-ratelimit-remaining": "59"},
        )

    client = create_mock_client(handler)
    user = client.get_user_profile("octocat")

    assert isinstance(user, GitHubUserModel)
    assert user.id == 583231
    assert user.login == "octocat"
    assert user.name == "The Octocat"
    assert user.bio == "GitHub mascot"
    assert user.public_repos == 8


def test_get_repository_normalization() -> None:
    """Verify fetching and normalizing a single repository metadata response."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/octocat/Hello-World"
        return httpx.Response(
            200,
            json={
                "id": 1296269,
                "name": "Hello-World",
                "full_name": "octocat/Hello-World",
                "description": "My first repository on GitHub!",
                "stargazers_count": 2500,
                "forks_count": 1200,
                "language": "C",
                "topics": ["octocat", "hello-world"],
                "license": {"name": "MIT License", "spdx_id": "MIT"},
            },
        )

    client = create_mock_client(handler)
    repo = client.get_repository("octocat", "Hello-World")

    assert isinstance(repo, GitHubRepositoryModel)
    assert repo.id == 1296269
    assert repo.name == "Hello-World"
    assert repo.full_name == "octocat/Hello-World"
    assert repo.stargazers_count == 2500
    assert repo.license_name == "MIT License"
    assert repo.topics == ["octocat", "hello-world"]


def test_get_repository_languages() -> None:
    """Verify fetching and normalizing repository language statistics."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/octocat/Hello-World/languages"
        return httpx.Response(
            200,
            json={"Python": 12000, "TypeScript": 8000, "HTML": 1500},
        )

    client = create_mock_client(handler)
    lang_stats = client.get_repository_languages("octocat", "Hello-World")

    assert isinstance(lang_stats, GitHubLanguageStatsModel)
    assert lang_stats.repository_name == "octocat/Hello-World"
    assert lang_stats.languages["Python"] == 12000
    assert lang_stats.total_bytes == 21500


def test_pagination_parsing_and_iteration() -> None:
    """Verify GitHub Link header pagination parsing and automatic iteration across pages."""
    link_header = (
        '<https://api.github.com/users/octocat/repos?page=2>; rel="next", '
        '<https://api.github.com/users/octocat/repos?page=3>; rel="last"'
    )
    meta = GitHubPagination.parse_link_header(link_header)

    assert meta.next_url == "https://api.github.com/users/octocat/repos?page=2"
    assert meta.last_url == "https://api.github.com/users/octocat/repos?page=3"

    call_count = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            return httpx.Response(
                200,
                json=[{"id": 1, "name": "repo1", "full_name": "octocat/repo1"}],
                headers={"Link": link_header},
            )
        return httpx.Response(
            200,
            json=[{"id": 2, "name": "repo2", "full_name": "octocat/repo2"}],
            headers={},
        )

    client = create_mock_client(handler)
    repos = client.get_user_repositories("octocat", per_page=1, auto_paginate=True)

    assert len(repos) == 2
    assert repos[0].name == "repo1"
    assert repos[1].name == "repo2"
    assert call_count == 2


def test_in_memory_cache_behavior() -> None:
    """Verify endpoint caching hits, misses, and invalidation."""
    cache = GitHubCache(enabled=True, ttl_seconds=60)
    assert cache.get("/user") is None
    assert cache.misses == 1

    cache.set("/user", {"id": 123})
    cached_data = cache.get("/user")
    assert cached_data == {"id": 123}
    assert cache.hits == 1

    cache.invalidate("/user")
    assert cache.get("/user") is None


def test_authentication_error_raises_without_retry() -> None:
    """Verify HTTP 401 raises AuthenticationError immediately without retrying."""
    attempts = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(401, json={"message": "Bad credentials"})

    client = create_mock_client(handler)

    with pytest.raises(AuthenticationError):
        client.get_authenticated_user()

    assert attempts == 1  # Did not attempt retry


def test_rate_limit_error_handling() -> None:
    """Verify HTTP 429 raises RateLimitError."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            json={"message": "API rate limit exceeded"},
            headers={"x-ratelimit-remaining": "0"},
        )

    client = create_mock_client(handler)

    with pytest.raises(RateLimitError):
        client.get_user_profile("octocat")


def test_rate_limit_endpoint() -> None:
    """Verify fetching current rate limit status."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/rate_limit"
        return httpx.Response(
            200,
            json={
                "resources": {
                    "core": {
                        "limit": 5000,
                        "remaining": 4990,
                        "reset": 1600000000,
                        "used": 10,
                    }
                }
            },
        )

    client = create_mock_client(handler)
    status = client.get_rate_limit()

    assert isinstance(status, RateLimitModel)
    assert status.limit == 5000
    assert status.remaining == 4990


def test_diagnostics_collection() -> None:
    """Verify diagnostics collection for requests and performance."""
    diag = GitHubDiagnostics()
    diag.record_request(duration_ms=150.0, success=True)
    diag.record_request(duration_ms=50.0, success=False)
    diag.record_retry()

    summary = diag.get_summary(cache_hits=2, cache_misses=1)

    assert summary["request_count"] == 2
    assert summary["failed_request_count"] == 1
    assert summary["retry_count"] == 1
    assert summary["cache_hits"] == 2
    assert summary["average_response_time_ms"] == 100.0
