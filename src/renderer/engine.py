"""
Rendering engine.
"""

from xml.etree.ElementTree import tostring

from src.dashboard.models import DashboardView
from src.renderer.card import CardRenderer
from src.renderer.header import HeaderRenderer
from src.renderer.layout import (
    CARD_HEIGHT,
    CARD_HORIZONTAL_GAP,
    CARD_VERTICAL_GAP,
    CARD_WIDTH,
    FIRST_CARD_X,
    FIRST_CARD_Y,
    MAX_COLUMNS,
)
from src.renderer.stats import StatsRenderer
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
        self._stats = StatsRenderer(self._theme)

    def render(
        self,
        dashboard: DashboardView,
    ) -> str:
        """Render the dashboard."""

        svg = self._canvas.create(
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
        )

        # Header
        self._header.render(
            svg,
            dashboard,
        )

        for index, repository in enumerate(dashboard.repositories):
            row = index // MAX_COLUMNS
            column = index % MAX_COLUMNS

            x = FIRST_CARD_X + column * (CARD_WIDTH + CARD_HORIZONTAL_GAP)
            y = FIRST_CARD_Y + row * (CARD_HEIGHT + CARD_VERTICAL_GAP)

            self._cards.render(
                svg,
                card=repository,
                x=x,
                y=y,
            )

        # Statistics panel
        self._stats.render(
            svg,
            dashboard,
            x=760,
            y=150,
        )

        return tostring(
            svg,
            encoding="unicode",
        )
