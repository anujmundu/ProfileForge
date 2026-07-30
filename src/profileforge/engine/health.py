"""Engine Health Audit and Status Reporting.

Reports lifecycle state, initialized components, configuration status, and startup metrics.
"""

from dataclasses import dataclass
from typing import Any

from profileforge.engine.lifecycle import LifecycleState


@dataclass(frozen=True)
class EngineHealth:
    """Immutable health audit report for the Engine subsystem."""

    lifecycle_state: LifecycleState
    initialized_components: list[str]
    configuration_status: str
    startup_duration_ms: float
    healthy: bool
    warnings_count: int = 0
    errors_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert health status report to a dictionary."""
        return {
            "healthy": self.healthy,
            "lifecycle_state": self.lifecycle_state.value,
            "initialized_components": self.initialized_components,
            "configuration_status": self.configuration_status,
            "startup_duration_ms": round(self.startup_duration_ms, 2),
            "warnings_count": self.warnings_count,
            "errors_count": self.errors_count,
        }
