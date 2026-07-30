"""Analytics Subsystem Exception Hierarchy.

Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class AnalyticsError(ProfileForgeError):
    """Base exception for all Analytics subsystem errors."""


class RepositoryAnalysisError(AnalyticsError):
    """Raised when repository scoring or ranking analysis fails."""


class LanguageAnalysisError(AnalyticsError):
    """Raised when language distribution analysis fails."""


class TechnologyInferenceError(AnalyticsError):
    """Raised when technology inference fails."""


class SkillInferenceError(AnalyticsError):
    """Raised when skill inference fails."""


class ActivityAnalysisError(AnalyticsError):
    """Raised when activity analysis fails."""
