"""
Rendering engine.
"""

from xml.etree.ElementTree import tostring

from src.dashboard.models import DashboardView
from src.renderer.svg.canvas import SvgCanvas
from src.renderer.header import HeaderRenderer


class RenderingEngine:
    """Coordinates SVG rendering."""

    def __init__(self) -> None:
        self._canvas = SvgCanvas()
        self._header = HeaderRenderer()

    def render(
        self,
        dashboard: DashboardView,
    ) -> str:
        """Render the dashboard as an SVG document."""

        svg = self._canvas.create(
            width=1200,
            height=630,
        )

        self._header.render(svg, dashboard)

        return tostring(
            svg,
            encoding="unicode",
        )