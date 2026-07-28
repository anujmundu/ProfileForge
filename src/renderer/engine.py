"""
Rendering engine.
"""

from xml.etree.ElementTree import tostring

from src.dashboard.models import DashboardView
from src.renderer.header import HeaderRenderer
from src.renderer.svg.canvas import SvgCanvas
from src.renderer.svg.styles import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    GITHUB_DARK,
)


class RenderingEngine:
    """Coordinates SVG rendering."""

    def __init__(self) -> None:
        self._canvas = SvgCanvas()
        self._theme = GITHUB_DARK
        self._header = HeaderRenderer(self._theme)

    def render(
        self,
        dashboard: DashboardView,
    ) -> str:
        """Render the dashboard as an SVG document."""

        svg = self._canvas.create(
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
        )

        self._header.render(
            svg,
            dashboard,
        )

        return tostring(
            svg,
            encoding="unicode",
        )