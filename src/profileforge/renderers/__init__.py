"""Rendering Subsystem.

Transforms presentation-independent models into concrete visual and textual artifacts.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from profileforge.renderers.diagnostics import RendererDiagnostics
from profileforge.renderers.exceptions import (
    JSONRenderError,
    MarkdownRenderError,
    RendererError,
    SVGRenderError,
    TemplateError,
    ThemeError,
)
from profileforge.renderers.json_renderer import JSONRenderer
from profileforge.renderers.markdown_renderer import MarkdownRenderer
from profileforge.renderers.models import (
    JSONArtifact,
    MarkdownArtifact,
    RenderedArtifacts,
    SVGArtifact,
)
from profileforge.renderers.orchestrator import RendererOrchestrator
from profileforge.renderers.renderer import BaseRenderer
from profileforge.renderers.svg_renderer import SVGRenderer
from profileforge.renderers.template_loader import TemplateLoader
from profileforge.renderers.theme_loader import ThemeLoader, ThemePalette

__all__ = [
    "BaseRenderer",
    "JSONArtifact",
    "JSONRenderError",
    "JSONRenderer",
    "MarkdownArtifact",
    "MarkdownRenderError",
    "MarkdownRenderer",
    "RenderedArtifacts",
    "RendererDiagnostics",
    "RendererError",
    "RendererOrchestrator",
    "SVGArtifact",
    "SVGRenderError",
    "SVGRenderer",
    "TemplateError",
    "TemplateLoader",
    "ThemeError",
    "ThemeLoader",
    "ThemePalette",
]
