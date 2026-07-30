"""Generators Subsystem Diagnostics Collector.

Collects execution duration, generated section counts, skipped sections, and warnings.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from typing import Any


class GeneratorDiagnostics:
    """Diagnostics telemetry tracker for the Generators subsystem."""

    def __init__(self) -> None:
        self.generation_duration_ms: float = 0.0
        self.generated_sections_count: int = 0
        self.skipped_sections: list[str] = []
        self.warnings: list[str] = []

    def record_skipped_section(self, section_name: str, reason: str) -> None:
        """Record a skipped section."""
        self.skipped_sections.append(f"{section_name}: {reason}")

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "generation_duration_ms": round(self.generation_duration_ms, 2),
            "generated_sections_count": self.generated_sections_count,
            "skipped_sections_count": len(self.skipped_sections),
            "skipped_sections": self.skipped_sections,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
        }
