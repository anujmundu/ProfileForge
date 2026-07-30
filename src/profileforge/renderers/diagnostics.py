"""Rendering Subsystem Diagnostics Collector.

Collects render execution duration, artifact counts, failed renderers, and warnings.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from typing import Any


class RendererDiagnostics:
    """Diagnostics telemetry tracker for the Rendering subsystem."""

    def __init__(self) -> None:
        self.render_duration_ms: float = 0.0
        self.rendered_artifacts_count: int = 0
        self.failed_renderers: list[str] = []
        self.warnings: list[str] = []

    def record_failure(self, renderer_name: str, reason: str) -> None:
        """Record a renderer failure."""
        self.failed_renderers.append(f"{renderer_name}: {reason}")

    def add_warning(self, message: str) -> None:
        """Record a diagnostic warning."""
        self.warnings.append(message)

    def get_summary(self) -> dict[str, Any]:
        """Generate structured diagnostics summary."""
        return {
            "render_duration_ms": round(self.render_duration_ms, 2),
            "rendered_artifacts_count": self.rendered_artifacts_count,
            "failed_renderers_count": len(self.failed_renderers),
            "failed_renderers": self.failed_renderers,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
        }
