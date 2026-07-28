"""
Rendering engine.
"""

from xml.etree.ElementTree import tostring

from src.dashboard.models import DashboardView
from src.renderer.svg.canvas import SvgCanvas


class RenderingEngine:
    """Coordinates SVG rendering."""

    def __init__(self) -> None:
        self._canvas = SvgCanvas()

    def render(
        self,
        dashboard: DashboardView,
    ) -> str:
        svg = self._canvas.create(
            width=1200,
            height=630,
        )

        return tostring(
            svg,
            encoding="unicode",
        )