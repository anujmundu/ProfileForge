"""Theme Loader for Rendering Subsystem.

Loads color palettes, typography, spacing, and styling options for SVG and Markdown presentation.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from dataclasses import dataclass
from typing import ClassVar

from profileforge.configuration import ThemesCategory
from profileforge.renderers.exceptions import ThemeError


@dataclass(frozen=True)
class ThemePalette:
    """Color palette and styling specifications for visual renderers."""

    name: str
    bg_color: str = "#0d1117"
    card_bg: str = "#161b22"
    border_color: str = "#30363d"
    text_primary: str = "#c9d1d9"
    text_secondary: str = "#8b949e"
    accent_color: str = "#58a6ff"
    success_color: str = "#3fb950"
    font_family: str = "Inter, sans-serif"


class ThemeLoader:
    """Loads and provides ThemePalette specifications."""

    THEMES: ClassVar[dict[str, ThemePalette]] = {
        "dark_glassmorphism": ThemePalette(
            name="dark_glassmorphism",
            bg_color="#0d1117",
            card_bg="#161b22",
            border_color="#30363d",
            text_primary="#c9d1d9",
            text_secondary="#8b949e",
            accent_color="#58a6ff",
            success_color="#3fb950",
            font_family="Inter, sans-serif",
        ),
        "light_minimal": ThemePalette(
            name="light_minimal",
            bg_color="#ffffff",
            card_bg="#f6f8fa",
            border_color="#d0d7de",
            text_primary="#24292f",
            text_secondary="#57606a",
            accent_color="#0969da",
            success_color="#1a7f37",
            font_family="Inter, sans-serif",
        ),
    }

    def __init__(self, theme_config: ThemesCategory | None = None) -> None:
        self._theme_config = theme_config or ThemesCategory()

    def get_active_theme(self) -> ThemePalette:
        """Retrieve active ThemePalette based on configuration."""
        theme_name = self._theme_config.active_theme
        if theme_name in self.THEMES:
            return self.THEMES[theme_name]
        return self.THEMES["dark_glassmorphism"]

    def get_theme(self, name: str) -> ThemePalette:
        """Retrieve ThemePalette by name."""
        if name not in self.THEMES:
            raise ThemeError(f"Theme '{name}' not found.")
        return self.THEMES[name]
