"""Analytics Subsystem Diagnostics Collector.

Collects analysis execution duration, scoring metrics, inference statistics, and warnings.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from typing import Any


class AnalyticsDiagnostics:
    """Diagnostics telemetry tracker for the Analytics subsystem."""

    def __init__(self) -> None:
        self.analysis_duration_ms: float = 0.0
        self.analyzed_repositories_count: int = 0
        self.skipped_repositories_count: int = 0
        self.inferred_skills_count: int = 0
        self.inferred_technologies_count: int = 0
        self.warnings: list[str] = []

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "analysis_duration_ms": round(self.analysis_duration_ms, 2),
            "analyzed_repositories_count": self.analyzed_repositories_count,
            "skipped_repositories_count": self.skipped_repositories_count,
            "inferred_skills_count": self.inferred_skills_count,
            "inferred_technologies_count": self.inferred_technologies_count,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
        }
