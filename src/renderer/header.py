"""
Header renderer.
"""

from xml.etree.ElementTree import Element

from src.dashboard.models import DashboardView
from src.renderer.svg.styles import Theme
from src.renderer.svg.text import add_text


class HeaderRenderer:
    """Renders the profile header."""

    def __init__(self, theme: Theme) -> None:
        self._theme = theme

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
            font_size=self._theme.title_font_size,
            font_weight=self._theme.title_weight,
        )

        add_text(
            svg,
            content=dashboard.bio or "",
            x=40,
            y=105,
            font_size=self._theme.subtitle_font_size,
            font_weight=self._theme.body_weight,
        )
