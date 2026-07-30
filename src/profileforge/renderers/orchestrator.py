"""Renderer Orchestrator Implementation.

Coordinates concrete renderers (Markdown, SVG, JSON) with strict failure isolation.
Governed by 09_RENDERING_SPECIFICATION.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import time

from profileforge.generators.models import PresentationModel
from profileforge.renderers.diagnostics import RendererDiagnostics
from profileforge.renderers.exceptions import RendererError
from profileforge.renderers.json_renderer import JSONRenderer
from profileforge.renderers.markdown_renderer import MarkdownRenderer
from profileforge.renderers.models import (
    JSONArtifact,
    MarkdownArtifact,
    RenderedArtifacts,
    SVGArtifact,
)
from profileforge.renderers.svg_renderer import SVGRenderer


class RendererOrchestrator:
    """Orchestrates rendering pipeline with failure isolation across renderers."""

    def __init__(self) -> None:
        self._markdown_renderer = MarkdownRenderer()
        self._svg_renderer = SVGRenderer()
        self._json_renderer = JSONRenderer()
        self._diagnostics = RendererDiagnostics()

    @property
    def diagnostics(self) -> RendererDiagnostics:
        """Get subsystem diagnostics tracker."""
        return self._diagnostics

    def render_presentation_model(
        self, presentation_model: PresentationModel
    ) -> RenderedArtifacts:
        """Render PresentationModel into RenderedArtifacts with failure isolation.

        Args:
            presentation_model: Canonical PresentationModel produced by Generators subsystem.

        Returns:
            RenderedArtifacts container storing all successfully rendered outputs.
        """
        start_time = time.perf_counter()

        markdown_art: MarkdownArtifact | None = None
        svg_arts: list[SVGArtifact] = []
        json_art: JSONArtifact | None = None
        artifact_count = 0

        # 1. Render Markdown README
        try:
            markdown_art = self._markdown_renderer.render(presentation_model)
            artifact_count += 1
        except RendererError as exc:
            self._diagnostics.record_failure("MarkdownRenderer", str(exc))

        # 2. Render SVG Visual Cards
        try:
            svg_arts = self._svg_renderer.render(presentation_model)
            artifact_count += len(svg_arts)
        except RendererError as exc:
            self._diagnostics.record_failure("SVGRenderer", str(exc))

        # 3. Render JSON Snapshot
        try:
            json_art = self._json_renderer.render(presentation_model)
            artifact_count += 1
        except RendererError as exc:
            self._diagnostics.record_failure("JSONRenderer", str(exc))

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        self._diagnostics.render_duration_ms = duration_ms
        self._diagnostics.rendered_artifacts_count = artifact_count

        return RenderedArtifacts(
            username=presentation_model.username,
            markdown_artifact=markdown_art,
            svg_artifacts=svg_arts,
            json_artifact=json_art,
            total_count=artifact_count,
        )
