"""Animation Engine Diagnostics Collector.

Collects execution duration, registered primitives, composed groups, and warnings.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from typing import Any


class AnimationDiagnostics:
    """Diagnostics telemetry tracker for the Animation Engine subsystem."""

    def __init__(self) -> None:
        self.generation_duration_ms: float = 0.0
        self.registered_primitives_count: int = 0
        self.composed_groups_count: int = 0
        self.warnings: list[str] = []

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "generation_duration_ms": round(self.generation_duration_ms, 2),
            "registered_primitives_count": self.registered_primitives_count,
            "composed_groups_count": self.composed_groups_count,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
        }
