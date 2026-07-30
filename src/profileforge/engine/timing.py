"""Phase Timing and Duration Tracker for Engine Subsystem.

Collects start timestamps, completion timestamps, and phase durations.
"""

import time
from dataclasses import dataclass, field
from typing import Any

from profileforge.engine.lifecycle import LifecyclePhase


@dataclass
class PhaseTimingRecord:
    """Record of an individual lifecycle phase execution duration."""

    phase: LifecyclePhase
    start_time: float
    end_time: float | None = None
    duration_ms: float | None = None

    def complete(self, end_timestamp: float | None = None) -> float:
        """Mark phase complete and compute duration in milliseconds."""
        self.end_time = time.perf_counter() if end_timestamp is None else end_timestamp
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        return self.duration_ms


@dataclass
class EngineTimingTracker:
    """Tracker for lifecycle phase timings and overall execution duration."""

    overall_start_time: float = field(default_factory=time.perf_counter)
    overall_end_time: float | None = None
    phase_records: dict[LifecyclePhase, PhaseTimingRecord] = field(
        default_factory=dict
    )

    def start_phase(self, phase: LifecyclePhase) -> PhaseTimingRecord:
        """Start timing a lifecycle phase."""
        record = PhaseTimingRecord(phase=phase, start_time=time.perf_counter())
        self.phase_records[phase] = record
        return record

    def complete_phase(self, phase: LifecyclePhase) -> float:
        """Complete timing a lifecycle phase."""
        record = self.phase_records.get(phase)
        if record is None:
            record = self.start_phase(phase)
        return record.complete()

    def complete_all(self) -> float:
        """Mark overall execution complete and return total duration in milliseconds."""
        self.overall_end_time = time.perf_counter()
        return (self.overall_end_time - self.overall_start_time) * 1000.0

    def get_summary(self) -> dict[str, Any]:
        """Return timing summary dictionary."""
        total_ms = (
            (self.overall_end_time - self.overall_start_time) * 1000.0
            if self.overall_end_time
            else (time.perf_counter() - self.overall_start_time) * 1000.0
        )
        return {
            "total_duration_ms": round(total_ms, 2),
            "phase_durations_ms": {
                phase.value: round(record.duration_ms, 2)
                for phase, record in self.phase_records.items()
                if record.duration_ms is not None
            },
        }
