"""
Shared SVG theme definitions.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Theme:
    """Visual theme for SVG rendering."""

    background: str
    surface: str
    border: str

    text_primary: str
    text_secondary: str

    accent: str

    title_font_size: int
    subtitle_font_size: int
    body_font_size: int
    small_font_size: int

    title_weight: str
    body_weight: str

    radius: int
    stroke_width: int


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 630


GITHUB_DARK = Theme(
    background="#0d1117",
    surface="#161b22",
    border="#30363d",
    text_primary="#f0f6fc",
    text_secondary="#8b949e",
    accent="#58a6ff",
    title_font_size=32,
    subtitle_font_size=18,
    body_font_size=16,
    small_font_size=13,
    title_weight="bold",
    body_weight="normal",
    radius=12,
    stroke_width=1,
)
