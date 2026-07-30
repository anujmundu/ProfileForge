"""Rendering Subsystem Exception Hierarchy.

Governed by 09_RENDERING_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class RendererError(ProfileForgeError):
    """Base exception for all Rendering subsystem errors."""


class MarkdownRenderError(RendererError):
    """Raised when Markdown README rendering fails."""


class SVGRenderError(RendererError):
    """Raised when SVG card rendering fails."""


class JSONRenderError(RendererError):
    """Raised when JSON serialization rendering fails."""


class TemplateError(RendererError):
    """Raised when template loading or processing fails."""


class ThemeError(RendererError):
    """Raised when theme loading or validation fails."""
