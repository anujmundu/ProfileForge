"""Engine Diagnostics and Telemetry Collector.

Collects startup timing, state transition events, subsystem status, warnings,
and generates structured execution summaries.
Independent of logging.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from profileforge.engine.lifecycle import LifecycleState
from profileforge.engine.timing import EngineTimingTracker


@dataclass
class TransitionEvent:
    """Record of a state transition event."""

    from_state: LifecycleState
    to_state: LifecycleState
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


@dataclass
class SubsystemStatusRecord:
    """Status record for a registered subsystem."""

    name: str
    initialized: bool
    status_message: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


class EngineDiagnostics:
    """Diagnostics collector for Engine execution, timing, and health auditing."""

    def __init__(self) -> None:
        self.timing_tracker: EngineTimingTracker = EngineTimingTracker()
        self.transition_events: list[TransitionEvent] = []
        self.subsystem_statuses: dict[str, SubsystemStatusRecord] = {}
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def record_transition(
        self, from_state: LifecycleState, to_state: LifecycleState
    ) -> None:
        """Record a state transition event."""
        self.transition_events.append(
            TransitionEvent(from_state=from_state, to_state=to_state)
        )

    def record_subsystem_status(
        self, name: str, initialized: bool, message: str = "OK"
    ) -> None:
        """Record initialization status for a subsystem."""
        self.subsystem_statuses[name] = SubsystemStatusRecord(
            name=name, initialized=initialized, status_message=message
        )

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured execution diagnostics summary."""
        timing_summary = self.timing_tracker.get_summary()
        return {
            "total_duration_ms": timing_summary["total_duration_ms"],
            "phase_durations_ms": timing_summary["phase_durations_ms"],
            "total_transitions": len(self.transition_events),
            "transitions": [
                {
                    "from": event.from_state.value,
                    "to": event.to_state.value,
                    "timestamp": event.timestamp,
                }
                for event in self.transition_events
            ],
            "subsystems": {
                name: {
                    "initialized": record.initialized,
                    "status": record.status_message,
                    "timestamp": record.timestamp,
                }
                for name, record in self.subsystem_statuses.items()
            },
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
            "errors_count": len(self.errors),
            "errors": self.errors,
        }
