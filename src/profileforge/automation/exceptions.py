"""Automation Subsystem Exception Hierarchy.

Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class AutomationError(ProfileForgeError):
    """Base exception for all Automation subsystem errors."""


class WorkflowError(AutomationError):
    """Raised when automation workflow execution fails."""


class PublishingError(AutomationError):
    """Raised when artifact publishing fails."""


class SchedulerError(AutomationError):
    """Raised when automation scheduling operations fail."""


class RetryError(AutomationError):
    """Raised when retry policy execution attempts are exhausted."""


class CancellationError(AutomationError):
    """Raised when workflow execution is cancelled via CancellationToken."""
