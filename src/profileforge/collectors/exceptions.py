"""Collectors Subsystem Exception Hierarchy.

Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class CollectorError(ProfileForgeError):
    """Base exception for all Collectors subsystem errors."""


class UserCollectionError(CollectorError):
    """Raised when user profile data collection fails."""


class RepositoryCollectionError(CollectorError):
    """Raised when repository metadata collection fails."""


class LanguageCollectionError(CollectorError):
    """Raised when repository language statistics collection fails."""


class ContributionCollectionError(CollectorError):
    """Raised when contribution data collection fails."""


class OrganizationCollectionError(CollectorError):
    """Raised when organization data collection fails."""
