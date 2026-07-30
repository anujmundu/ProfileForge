"""Unit tests for Collectors Subsystem using mocked GitHubClient.

All network calls are strictly mocked via httpx.MockTransport.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 08_ANALYTICS_SPECIFICATION.md.
"""

from typing import Any

import httpx
import pytest

from profileforge.collectors import (
    CollectionSnapshot,
    CollectorDiagnostics,
    CollectorOrchestrator,
    ContributionCollection,
    ContributionCollector,
    LanguageCollection,
    LanguageCollector,
    OrganizationCollection,
    OrganizationCollector,
    RepositoryCollection,
    RepositoryCollector,
    User,
    UserCollectionError,
    UserCollector,
)
from profileforge.github import GitHubClient


def create_mock_github_client(handler: Any) -> GitHubClient:
    """Helper to create a GitHubClient with a mock transport."""
    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(
        base_url="https://api.github.com",
        transport=transport,
        follow_redirects=True,
    )
    return GitHubClient(http_client=http_client)


def test_user_collector() -> None:
    """Verify UserCollector retrieves and constructs canonical User domain object."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": 101,
                "login": "dev_user",
                "name": "Dev User",
                "bio": "Software Craftsman",
                "public_repos": 12,
            },
        )

    client = create_mock_github_client(handler)
    collector = UserCollector(client)
    user = collector.collect("dev_user")

    assert isinstance(user, User)
    assert user.id == 101
    assert user.login == "dev_user"
    assert user.name == "Dev User"
    assert user.bio == "Software Craftsman"
    assert user.public_repos == 12


def test_user_collector_failure() -> None:
    """Verify UserCollector raises UserCollectionError on API failure."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found"})

    client = create_mock_github_client(handler)
    collector = UserCollector(client)

    with pytest.raises(UserCollectionError):
        collector.collect("non_existent_user")


def test_repository_collector() -> None:
    """Verify RepositoryCollector retrieves repositories and produces RepositoryCollection."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {
                    "id": 1001,
                    "name": "project-alpha",
                    "full_name": "dev_user/project-alpha",
                    "stargazers_count": 45,
                    "language": "Python",
                },
                {
                    "id": 1002,
                    "name": "project-beta",
                    "full_name": "dev_user/project-beta",
                    "stargazers_count": 12,
                    "language": "TypeScript",
                },
            ],
        )

    client = create_mock_github_client(handler)
    collector = RepositoryCollector(client)
    repo_coll = collector.collect("dev_user", auto_paginate=False)

    assert isinstance(repo_coll, RepositoryCollection)
    assert repo_coll.total_count == 2
    assert repo_coll.repositories[0].name == "project-alpha"
    assert repo_coll.repositories[1].stargazers_count == 12


def test_language_collector() -> None:
    """Verify LanguageCollector aggregates repository language byte counts."""

    def handler(request: httpx.Request) -> httpx.Response:
        if "project-alpha" in request.url.path:
            return httpx.Response(200, json={"Python": 10000, "HTML": 2000})
        return httpx.Response(200, json={"Python": 5000, "TypeScript": 15000})

    client = create_mock_github_client(handler)

    def repo_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {"id": 1, "name": "project-alpha", "full_name": "dev_user/project-alpha"},
                {"id": 2, "name": "project-beta", "full_name": "dev_user/project-beta"},
            ],
        )

    repo_client = create_mock_github_client(repo_handler)
    repo_collector_with_client = RepositoryCollector(repo_client)
    repo_coll = repo_collector_with_client.collect("dev_user", auto_paginate=False)

    lang_collector = LanguageCollector(client)
    lang_coll = lang_collector.collect("dev_user", repo_coll)

    assert isinstance(lang_coll, LanguageCollection)
    assert lang_coll.language_bytes["Python"] == 15000
    assert lang_coll.language_bytes["TypeScript"] == 15000
    assert lang_coll.language_bytes["HTML"] == 2000
    assert lang_coll.total_bytes == 32000


def test_contribution_collector() -> None:
    """Verify ContributionCollector explicitly reports metrics or absence."""
    client = create_mock_github_client(lambda _r: httpx.Response(200, json={}))
    collector = ContributionCollector(client)
    contrib_coll = collector.collect("dev_user")

    assert isinstance(contrib_coll, ContributionCollection)
    assert contrib_coll.has_data is False


def test_organization_collector() -> None:
    """Verify OrganizationCollector retrieves organization membership metadata."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/users/dev_user/orgs"
        return httpx.Response(
            200,
            json=[
                {
                    "id": 999,
                    "login": "acme-corp",
                    "description": "Acme Open Source",
                    "avatar_url": "https://avatars.githubusercontent.com/u/999",
                }
            ],
        )

    client = create_mock_github_client(handler)
    collector = OrganizationCollector(client)
    org_coll = collector.collect("dev_user")

    assert isinstance(org_coll, OrganizationCollection)
    assert org_coll.total_count == 1
    assert org_coll.organizations[0]["login"] == "acme-corp"


def test_collector_orchestrator() -> None:
    """Verify CollectorOrchestrator runs the complete pipeline and produces CollectionSnapshot."""

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/users/octocat":
            return httpx.Response(
                200,
                json={"id": 583231, "login": "octocat", "name": "The Octocat"},
            )
        if path == "/users/octocat/repos":
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 1,
                        "name": "Hello-World",
                        "full_name": "octocat/Hello-World",
                        "stargazers_count": 100,
                    }
                ],
            )
        if path == "/repos/octocat/Hello-World/languages":
            return httpx.Response(200, json={"C": 5000})
        if path == "/users/octocat/orgs":
            return httpx.Response(200, json=[])

        return httpx.Response(404, json={"message": "Not Found"})

    client = create_mock_github_client(handler)
    orchestrator = CollectorOrchestrator(client)
    snapshot = orchestrator.collect_user_snapshot("octocat")

    assert isinstance(snapshot, CollectionSnapshot)
    assert snapshot.username == "octocat"
    assert snapshot.user.login == "octocat"
    assert snapshot.repositories.total_count == 1
    assert snapshot.languages.language_bytes["C"] == 5000
    assert orchestrator.diagnostics.repositories_collected == 1


def test_collector_diagnostics() -> None:
    """Verify CollectorDiagnostics records failures and summary outputs."""
    diag = CollectorDiagnostics()
    diag.record_failure("OrgCollector", "Network timeout")
    diag.add_warning("Rate limit approaching threshold")

    summary = diag.get_summary()

    assert summary["failed_collections_count"] == 1
    assert summary["warnings_count"] == 1
    assert "OrgCollector: Network timeout" in summary["failed_collections"]
