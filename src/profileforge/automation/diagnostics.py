"""Automation Subsystem Diagnostics Collector.

Collects workflow execution duration, per-stage durations, retry attempts, and warnings.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from typing import Any


class AutomationDiagnostics:
    """Diagnostics telemetry tracker for the Automation subsystem."""

    def __init__(self) -> None:
        self.total_execution_duration_ms: float = 0.0
        self.stage_durations: dict[str, float] = {}
        self.retry_attempts_count: int = 0
        self.published_artifacts_count: int = 0
        self.warnings: list[str] = []
        self.failures: list[str] = []

    def record_stage_duration(self, stage_name: str, duration_ms: float) -> None:
        """Record execution duration for a stage."""
        self.stage_durations[stage_name] = round(duration_ms, 2)

    def record_retry_attempt(self) -> None:
        """Increment retry attempt counter."""
        self.retry_attempts_count += 1

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def record_failure(self, stage_name: str, reason: str) -> None:
        """Record a stage failure."""
        self.failures.append(f"{stage_name}: {reason}")

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "total_execution_duration_ms": round(self.total_execution_duration_ms, 2),
            "stage_durations": self.stage_durations,
            "retry_attempts_count": self.retry_attempts_count,
            "published_artifacts_count": self.published_artifacts_count,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
            "failures_count": len(self.failures),
            "failures": self.failures,
        }
