"""Engine Subsystem Exception Hierarchy.

Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class EngineError(ProfileForgeError):
    """Base exception for all Engine subsystem errors."""


class BootstrapError(EngineError):
    """Raised when engine bootstrap fails."""


class LifecycleError(EngineError):
    """Raised when an invalid state transition or lifecycle violation occurs."""


class DependencyError(EngineError):
    """Raised when dependency registration or retrieval fails."""


class InitializationError(EngineError):
    """Raised when service or subsystem initialization fails."""
