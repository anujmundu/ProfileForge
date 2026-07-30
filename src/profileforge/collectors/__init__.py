"""Collectors Subsystem.

Retrieves and assembles normalized GitHub data into canonical domain collection models.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.collectors.contribution_collector import ContributionCollector
from profileforge.collectors.diagnostics import CollectorDiagnostics
from profileforge.collectors.exceptions import (
    CollectorError,
    ContributionCollectionError,
    LanguageCollectionError,
    OrganizationCollectionError,
    RepositoryCollectionError,
    UserCollectionError,
)
from profileforge.collectors.language_collector import LanguageCollector
from profileforge.collectors.models import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    Repository,
    RepositoryCollection,
    User,
)
from profileforge.collectors.orchestrator import CollectorOrchestrator
from profileforge.collectors.organization_collector import OrganizationCollector
from profileforge.collectors.repository_collector import RepositoryCollector
from profileforge.collectors.user_collector import UserCollector

__all__ = [
    "CollectionSnapshot",
    "CollectorDiagnostics",
    "CollectorError",
    "CollectorOrchestrator",
    "ContributionCollection",
    "ContributionCollectionError",
    "ContributionCollector",
    "LanguageCollection",
    "LanguageCollectionError",
    "LanguageCollector",
    "OrganizationCollection",
    "OrganizationCollectionError",
    "OrganizationCollector",
    "Repository",
    "RepositoryCollection",
    "RepositoryCollectionError",
    "RepositoryCollector",
    "User",
    "UserCollectionError",
    "UserCollector",
]
