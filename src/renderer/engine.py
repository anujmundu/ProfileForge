"""
Rendering engine.
"""

from xml.etree.ElementTree import tostring

from src.dashboard.models import DashboardView
from src.renderer.card import CardRenderer
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
        self._cards = CardRenderer(self._theme)

    def render(
        self,
        dashboard: DashboardView,
    ) -> str:
        """Render the dashboard as an SVG document."""

        # 1. Create the SVG canvas FIRST
        svg = self._canvas.create(
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
        )

        # 2. Render the header
        self._header.render(
            svg,
            dashboard,
        )

        # 3. Render the first repository card (if available)
        if dashboard.repositories:
            self._cards.render(
                svg,
                card=dashboard.repositories[0],
                x=40,
                y=150,
            )

        # 4. Serialize the SVG
        return tostring(
            svg,
            encoding="unicode",
        )