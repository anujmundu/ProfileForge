"""Collectors Subsystem Diagnostics Collector.

Collects execution metrics, item counts, failed/skipped collections, and warnings.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from typing import Any


class CollectorDiagnostics:
    """Collector diagnostics telemetry tracker."""

    def __init__(self) -> None:
        self.execution_duration_ms: float = 0.0
        self.repositories_collected: int = 0
        self.organizations_collected: int = 0
        self.api_requests_consumed: int = 0
        self.failed_collections: list[str] = []
        self.skipped_collections: list[str] = []
        self.warnings: list[str] = []

    def record_failure(self, collector_name: str, reason: str) -> None:
        """Record a collection failure."""
        self.failed_collections.append(f"{collector_name}: {reason}")

    def record_skipped(self, collector_name: str, reason: str) -> None:
        """Record a skipped collection."""
        self.skipped_collections.append(f"{collector_name}: {reason}")

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "execution_duration_ms": round(self.execution_duration_ms, 2),
            "repositories_collected": self.repositories_collected,
            "organizations_collected": self.organizations_collected,
            "api_requests_consumed": self.api_requests_consumed,
            "failed_collections_count": len(self.failed_collections),
            "failed_collections": self.failed_collections,
            "skipped_collections_count": len(self.skipped_collections),
            "skipped_collections": self.skipped_collections,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
        }
