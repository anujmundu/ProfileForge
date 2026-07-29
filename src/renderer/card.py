"""
Repository card renderer.
"""

from xml.etree.ElementTree import Element

from src.dashboard.models import RepositoryCard
from src.renderer.svg.rectangle import add_rectangle
from src.renderer.svg.styles import Theme
from src.renderer.svg.text import add_text


class CardRenderer:
    """Renders a repository card."""

    def __init__(self, theme: Theme) -> None:
        self._theme = theme

    def render(
        self,
        svg: Element,
        *,
        card: RepositoryCard,
        x: int,
        y: int,
        width: int = 520,
        height: int = 150,
    ) -> None:
        """Render a single repository card."""

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
            content=card.name,
            x=x + 20,
            y=y + 35,
            font_size=self._theme.subtitle_font_size,
            font_weight=self._theme.title_weight,
        )

        add_text(
            svg,
            content=card.description or "",
            x=x + 20,
            y=y + 65,
            font_size=self._theme.body_font_size,
        )

        add_text(
            svg,
            content=f"Language: {card.language or 'Unknown'}",
            x=x + 20,
            y=y + 100,
            font_size=self._theme.small_font_size,
        )

        add_text(
            svg,
            content=f"★ {card.stars}   Forks: {card.forks}",
            x=x + 20,
            y=y + 125,
            font_size=self._theme.small_font_size,
        )
