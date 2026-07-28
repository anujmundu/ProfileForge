"""
Common renderer interfaces.
"""

from typing import Protocol
from xml.etree.ElementTree import Element

from src.dashboard.models import DashboardView


class RendererComponent(Protocol):
    """Protocol implemented by all renderer components."""

    def render(
        self,
        svg: Element,
        dashboard: DashboardView,
    ) -> None:
        """Render onto the SVG canvas."""
        ...