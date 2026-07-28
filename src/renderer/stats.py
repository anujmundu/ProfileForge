"""
Statistics panel renderer.
"""

from xml.etree.ElementTree import Element

from src.dashboard.models import DashboardView
from src.renderer.svg.rectangle import add_rectangle
from src.renderer.svg.styles import Theme
from src.renderer.svg.text import add_text


class StatsRenderer:
    """Render dashboard statistics."""

    def __init__(self, theme: Theme) -> None:
        self._theme = theme

    def render(
        self,
        svg: Element,
        dashboard: DashboardView,
        *,
        x: int,
        y: int,
        width: int = 260,
        height: int = 140,
    ) -> None:
        """Render the statistics panel."""

        add_rectangle(
            svg,
            x=x,
            y=y,
            width=width,
            height=height,
            fill=self._theme.surface,
            stroke=self._theme.border,
            stroke_width=self._theme.stroke_width,
            rx=self._theme.radius,
            ry=self._theme.radius,
        )

        add_text(
            svg,
            content="GitHub Statistics",
            x=x + 20,
            y=y + 30,
            font_size=self._theme.subtitle_font_size,
            font_weight=self._theme.title_weight,
        )

        add_text(
            svg,
            content=f"Repositories : {dashboard.total_repositories}",
            x=x + 20,
            y=y + 65,
            font_size=self._theme.body_font_size,
        )

        add_text(
            svg,
            content=f"Stars        : {dashboard.total_stars}",
            x=x + 20,
            y=y + 90,
            font_size=self._theme.body_font_size,
        )

        add_text(
            svg,
            content=f"Forks        : {dashboard.total_forks}",
            x=x + 20,
            y=y + 115,
            font_size=self._theme.body_font_size,
        )