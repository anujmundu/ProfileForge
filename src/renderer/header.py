"""
Header renderer.
"""

from xml.etree.ElementTree import Element

from src.dashboard.models import DashboardView
from src.renderer.svg.text import add_text
from src.renderer.svg.styles import (
    TITLE_FONT_SIZE,
    SUBTITLE_FONT_SIZE,
    FONT_WEIGHT_BOLD,
)


class HeaderRenderer:
    """Renders the profile header."""

    def render(
        self,
        svg: Element,
        dashboard: DashboardView,
    ) -> None:
        """Render the dashboard header."""

        add_text(
            svg,
            content=dashboard.name or dashboard.username,
            x=40,
            y=70,
            font_size=TITLE_FONT_SIZE,
            font_weight=FONT_WEIGHT_BOLD,
        )

        add_text(
            svg,
            content=dashboard.bio or "",
            x=40,
            y=105,
            font_size=SUBTITLE_FONT_SIZE,
        )