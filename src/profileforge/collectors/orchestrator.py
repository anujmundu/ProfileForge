"""Collection Orchestrator Implementation.

Coordinates modular collectors in deterministic order to assemble a complete CollectionSnapshot.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import time

from profileforge.collectors.contribution_collector import ContributionCollector
from profileforge.collectors.diagnostics import CollectorDiagnostics
from profileforge.collectors.exceptions import CollectorError
from profileforge.collectors.language_collector import LanguageCollector
from profileforge.collectors.models import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    RepositoryCollection,
    User,
)
from profileforge.collectors.organization_collector import OrganizationCollector
from profileforge.collectors.repository_collector import RepositoryCollector
from profileforge.collectors.user_collector import UserCollector
from profileforge.github import GitHubClient


class CollectorOrchestrator:
    """Single orchestration entry point managing collection order and snapshot assembly."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client
        self._user_collector = UserCollector(client)
        self._repo_collector = RepositoryCollector(client)
        self._lang_collector = LanguageCollector(client)
        self._contrib_collector = ContributionCollector(client)
        self._org_collector = OrganizationCollector(client)
        self._diagnostics = CollectorDiagnostics()

    @property
    def diagnostics(self) -> CollectorDiagnostics:
        """Get subsystem diagnostics tracker."""
        return self._diagnostics

    def collect_user_snapshot(self, username: str) -> CollectionSnapshot:
        """Execute complete collection pipeline for a GitHub user and construct CollectionSnapshot.

        Args:
            username: Target GitHub username.

        Returns:
            Immutable CollectionSnapshot containing all collected domain models.

        Raises:
            CollectorError: If primary user or repository collection fails.
        """
        start_time = time.perf_counter()

        # 1. User Collector
        user: User = self._user_collector.collect(username)

        # 2. Repository Collector
        repos: RepositoryCollection = self._repo_collector.collect(username)
        self._diagnostics.repositories_collected = repos.total_count

        # 3. Language Collector
        languages: LanguageCollection = self._lang_collector.collect(username, repos)

        # 4. Contribution Collector
        contributions: ContributionCollection = self._contrib_collector.collect(username)

        # 5. Organization Collector
        try:
            organizations: OrganizationCollection = self._org_collector.collect(username)
            self._diagnostics.organizations_collected = organizations.total_count
        except CollectorError as exc:
            self._diagnostics.record_failure("OrganizationCollector", str(exc))
            organizations = OrganizationCollection(username=username, organizations=[], total_count=0)

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        self._diagnostics.execution_duration_ms = duration_ms
        self._diagnostics.api_requests_consumed = self._client.diagnostics.request_count

        return CollectionSnapshot(
            username=username,
            user=user,
            repositories=repos,
            languages=languages,
            contributions=contributions,
            organizations=organizations,
        )
